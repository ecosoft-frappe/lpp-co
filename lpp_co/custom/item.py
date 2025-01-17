# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from erpnext.stock.doctype.item.item import Item
from frappe import _


class ItemLPP(Item):

	def validate_item_specification_line(self):
		# Validate unique parameter in the item
		specifications = [line.specification for line in self.custom_item_specification_line]
		if len(specifications) != len(set(specifications)):
			frappe.throw(_("Parameter must be unique"))

	def validate(self):
		self.validate_item_specification_line()
		super().validate()

	@frappe.whitelist()
	def get_item_quality_specification(self):
		# Find item specification groups related to this item
		param_groups = self.get_related_quality_param_groups()
		params = frappe.get_all(
      		"Quality Inspection Parameter",
        	filters={"parameter_group": ["in", param_groups], "custom_is_item_spec": 1},
         	pluck="name",
        	order_by="name"
        )
		return params

	def get_related_quality_param_groups(self):
		# Loop throuh item_group and all its parents and get quality inspetion param groups
		param_groups = []
		def fetch_parent_groups(item_group):
			param_group = frappe.get_value("Item Group", item_group, "custom_quality_inspection_parameter_group")
			print(param_group)
			if param_group:
				param_groups.append(param_group)
			parent_item_group = frappe.get_value("Item Group", item_group, "parent_item_group")
			if parent_item_group:
				fetch_parent_groups(parent_item_group)  # Recursive call to fetch its parent
		fetch_parent_groups(self.item_group)
		return list(set(param_groups))

