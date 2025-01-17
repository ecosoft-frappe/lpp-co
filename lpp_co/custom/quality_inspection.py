# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt
import json
import frappe
from erpnext.stock.doctype.quality_inspection.quality_inspection import QualityInspection
from frappe import _
from frappe.utils import get_link_to_form

QC_TEMPLATE_FIELDS = [
	"custom_visual_inspection",
	"custom_functional_testing",
	"custom_specification_inspection"
]

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
		# Still not sure if we need to check?
		# ------------------------------------
		# doc = frappe.get_doc(self.reference_type, self.reference_name)
		# if self.reference_type == "Purchase Receipt" and doc.get("docstatus", 0) == 1:
		# 	if not frappe.get_cached_value(
		# 		"Item", self.item_code, "custom_inspection_required_after_purchase_receipt"
		# 	):
		# 		frappe.throw(
		# 			_(
		# 				"'Inspection Required after Purchase Receipt' has disabled for the item {0}, no need to create the QI"
		# 			).format(get_link_to_form("Item", self.item_code))
		# 		)
		# else:
		# 	super().validate_inspection_required()
		return

	def on_update(self):
		self.reset_quality_inspection_results()

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
		for tmpl_field in QC_TEMPLATE_FIELDS:
			if prev_doc.get(tmpl_field) != self.get(tmpl_field):
				return True

		# Compare sample quantity
		if prev_doc.sample_size != self.sample_size:
			return True

		return False

	def _create_quality_inspection_results(self):
		"""Create Quality Inspection Results based on templates."""
		for tmpl_field in QC_TEMPLATE_FIELDS:
			template_name = self.get(tmpl_field)
			if not template_name:
				continue

			# Fetch the template and create results for each parameter
			doc_template = frappe.get_doc("Quality Inspection Template", template_name)
			for row in doc_template.item_quality_inspection_parameter:
				result = frappe.get_doc({
					"doctype": "Quality Inspection Result",
					"quality_inspection": self.name,
					"quality_inspection_template": doc_template.name,
					"parameter": row.specification
				})
				for i in range(self.sample_size):
					result.append("readings", {})  # Add bland row
				result.insert(ignore_permissions=True)

	@frappe.whitelist()
	def get_visual_inspection_html(self):
		data = frappe.get_all(
			"Quality Inspection Result",
			fields=["parameter", "nominal", "delta_plus", "delta_minus", "qty_accepted", "qty_rejected"],
			filters={
				"quality_inspection": self.name,
				"quality_inspection_template": self.custom_visual_inspection
			},
			order_by="name"
		)
		return frappe.render_template("lpp_co/custom/inspection_result/visual_inspection.html", {"data": data})

	@frappe.whitelist()
	def get_specification_inspection_html(self):
		data = frappe.get_all(
			"Quality Inspection Result",
			fields=["parameter", "nominal", "delta_plus", "delta_minus", "qty_accepted", "qty_rejected"],
			filters={
				"quality_inspection": self.name,
				"quality_inspection_template": self.custom_specification_inspection
			},
			order_by="name"
		)
		return frappe.render_template("lpp_co/custom/inspection_result/specification_inspection.html", {"data": data})

	@frappe.whitelist()
	def get_functional_testing_html(self):
		data = frappe.get_all(
			"Quality Inspection Result",
			fields=["parameter", "nominal", "delta_plus", "delta_minus", "qty_accepted", "qty_rejected"],
			filters={
				"quality_inspection": self.name,
				"quality_inspection_template": self.custom_functional_testing
			},
			order_by="name"
		)
		return frappe.render_template("lpp_co/custom/inspection_result/functional_testing.html", {"data": data})
