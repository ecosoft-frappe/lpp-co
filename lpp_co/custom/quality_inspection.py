# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from erpnext.stock.doctype.quality_inspection.quality_inspection import QualityInspection
from frappe import _
from frappe.utils import get_link_to_form


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
		doc = frappe.get_doc(self.reference_type, self.reference_name)
		if self.reference_type == "Purchase Receipt" and doc.get("docstatus", 0) == 1:
			if not frappe.get_cached_value(
				"Item", self.item_code, "custom_inspection_required_after_purchase_receipt"
			):
				frappe.throw(
					_(
						"'Inspection Required after Purchase Receipt' has disabled for the item {0}, no need to create the QI"
					).format(get_link_to_form("Item", self.item_code))
				)
		else:
			super().validate_inspection_required()
