# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt
import frappe
from frappe.utils import cint, cstr
from erpnext.stock.doctype.quality_inspection.quality_inspection import QualityInspection
from frappe import _


class QualityInspectionLPP(QualityInspection):

	def get_formula_evaluation_data(self, reading):
		data = super().get_formula_evaluation_data(reading)
		# Item specification line reading
		item = frappe.get_doc("Item", self.item_code)
		specification_lines = item.as_dict().custom_item_specification_line
		specification_line_dict = {line.pop("specification"): line for line in specification_lines}
		specification_line = specification_line_dict.get(reading.specification, {})
		data.update(
			{
				"nominal": specification_line.get("nominal", 0.0),
				"delta_plus": specification_line.get("delta_plus", 0.0),
				"delta_minus": specification_line.get("delta_minus", 0.0),
			}
		)
		return data

	def validate_inspection_required(self):
		# For LPP, there is no checking on QI
		return

	def on_update(self):
		self.reset_quality_inspection_results()
		self.set_purchase_receipt_quantity()

	# Override, as we don't need to use readings, but use QI Result instead.
	@frappe.whitelist()
	def get_item_specification_details(self):
		return
	# --
 
	def set_purchase_receipt_quantity(self):
		if self.reference_type != "Purchase Receipt" or not self.reference_name:
			return
		# Fetch the Purchase Receipt Item linked to this Quality Inspection
		purchase_receipt_item = frappe.db.get_value(
			"Purchase Receipt Item",
			{"parent": self.reference_name, "name": self.child_row_reference},
			["qty", "uom"],
			as_dict=True,
		)
		if purchase_receipt_item:
			frappe.db.set_value("Quality Inspection", self.name, "custom_stock_quantity", purchase_receipt_item["qty"])
			frappe.db.set_value("Quality Inspection", self.name, "custom_stock_uom", purchase_receipt_item["uom"])
			self.reload()

	def reset_quality_inspection_results(self):
		# Check if reset is necessary
		prev_doc = self.get_doc_before_save()
		if not self._should_reset_quality_inspection_results(prev_doc):
			return

		# Delete existing Quality Inspection Results
		frappe.db.delete("Quality Inspection Result", {"quality_inspection": self.name})

		# Recreate Quality Inspection Results
		self._create_quality_inspection_results()

	def _should_reset_quality_inspection_results(self, prev_doc):
		"""Check if Quality Inspection Results need to be reset."""
		if not prev_doc:
			return True  # Reset if there is no previous document

		# Compare template fields in the current and previous document
		if prev_doc.get("quality_inspection_template") != self.get("quality_inspection_template"):
			return True

		# Compare sample quantity
		if prev_doc.sample_size != self.sample_size:
			return True

		return False

	def _create_quality_inspection_results(self):
		"""Create Quality Inspection Results based on templates."""
		template_name = self.get("quality_inspection_template")
		if not template_name:
			return

		# Fetch the template and create results for each parameter
		doc_template = frappe.get_doc("Quality Inspection Template", template_name)
		for row in doc_template.item_quality_inspection_parameter:
			result = frappe.get_doc({
				"doctype": "Quality Inspection Result",
				"quality_inspection": self.name,
				"quality_inspection_template": doc_template.name,
				"parameter": row.specification,
				"inspection_method": row.custom_inspection_method
			})
			for i in range(self.sample_size):
				result.append("readings", {})  # Add bland row
			result.insert(ignore_permissions=True)

	@frappe.whitelist()
	def get_visual_inspection_html(self):
		data = frappe.get_all(
			"Quality Inspection Result",
			fields=["parameter", "nominal", "delta_plus", "delta_minus", "qty_accepted", "qty_rejected", "remarks"],
			filters={
				"quality_inspection": self.name,
				"quality_inspection_template": self.quality_inspection_template,
				"inspection_method": "Visual Inspection"
			},
			order_by="name"
		)
		return frappe.render_template("lpp_co/custom/inspection_result.html", {"data": data})

	@frappe.whitelist()
	def get_specification_inspection_html(self):
		data = frappe.get_all(
			"Quality Inspection Result",
			fields=["parameter", "nominal", "delta_plus", "delta_minus", "qty_accepted", "qty_rejected", "remarks"],
			filters={
				"quality_inspection": self.name,
				"quality_inspection_template": self.quality_inspection_template,
				"inspection_method": "Specification Inspection"
			},
			order_by="name"
		)
		return frappe.render_template("lpp_co/custom/inspection_result.html", {"data": data})

	@frappe.whitelist()
	def get_functional_testing_html(self):
		data = frappe.get_all(
			"Quality Inspection Result",
			fields=["parameter", "nominal", "delta_plus", "delta_minus", "qty_accepted", "qty_rejected", "remarks"],
			filters={
				"quality_inspection": self.name,
				"quality_inspection_template": self.quality_inspection_template,
				"inspection_method": "Functional Testing"
			},
			order_by="name"
		)
		return frappe.render_template("lpp_co/custom/inspection_result.html", {"data": data})


# Override function, to remove inspection requried condition.
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def item_query(doctype, txt, searchfield, start, page_len, filters):
	from frappe.desk.reportview import get_match_cond

	from_doctype = cstr(filters.get("from"))
	if not from_doctype or not frappe.db.exists("DocType", from_doctype):
		return []

	mcond = get_match_cond(from_doctype)
	cond, qi_condition = "", "and (quality_inspection is null or quality_inspection = '')"

	if filters.get("parent"):
		# In LPP we do not need to worry about inspection requirement.
		# if (
		# 	from_doctype in ["Purchase Invoice Item", "Purchase Receipt Item"]
		# 	and filters.get("inspection_type") != "In Process"
		# ):
		# 	cond = """and item_code in (select name from `tabItem` where
		# 		inspection_required_before_purchase = 1)"""
		# elif (
		# 	from_doctype in ["Sales Invoice Item", "Delivery Note Item"]
		# 	and filters.get("inspection_type") != "In Process"
		# ):
		# 	cond = """and item_code in (select name from `tabItem` where
		# 		inspection_required_before_delivery = 1)"""
		# elif from_doctype == "Stock Entry Detail":
		# 	cond = """and s_warehouse is null"""
		if from_doctype == "Stock Entry Detail":
			cond = """and s_warehouse is null"""
		# --

		if from_doctype in ["Supplier Quotation Item"]:
			qi_condition = ""

		return frappe.db.sql(
			f"""
				SELECT item_code, item_name
				FROM `tab{from_doctype}`
				WHERE parent=%(parent)s and docstatus < 2
    			and (item_code like %(txt)s or item_name like %(txt)s)
				{qi_condition} {cond} {mcond}
				ORDER BY item_code limit {cint(page_len)} offset {cint(start)}
			""",
			{"parent": filters.get("parent"), "txt": "%%%s%%" % txt},
		)

	elif filters.get("reference_name"):
		conditions = "" if from_doctype == "Job Card" else f"{qi_condition} {cond} {mcond}"
		
		return frappe.db.sql(
			f"""
				SELECT production_item
				FROM `tab{from_doctype}`
				WHERE name = %(reference_name)s and docstatus < 2 and production_item like %(txt)s
				{conditions}
				ORDER BY production_item
				limit {cint(page_len)} offset {cint(start)}
			""",
			{"reference_name": filters.get("reference_name"), "txt": "%%%s%%" % txt},
		)
