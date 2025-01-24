# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from erpnext.stock.doctype.item.item import Item
from frappe.utils.nestedset import get_ancestors_of
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
		item_groups = get_ancestors_of("Item Group", self.item_group)
		item_groups.append(self.item_group)
		params = frappe.get_all(
      		"Quality Inspection Parameter",
        	filters=[
				["Quality Inspection Parameter Item Group",
     			 "item_group", "in", item_groups]
			],
         	pluck="name",
        	order_by="name"
        )
		return list(set(params))

