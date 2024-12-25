# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from erpnext.stock.doctype.quality_inspection.quality_inspection import QualityInspection


class LPPQualityInspection(QualityInspection):
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
