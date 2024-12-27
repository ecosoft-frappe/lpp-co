# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from erpnext.stock.doctype.item.item import Item
from frappe import _


class LPPItem(Item):
	def validate_item_specification_line(self):
		# Validate unique parameter in the item
		specifications = [line.specification for line in self.custom_item_specification_line]
		if len(specifications) != len(set(specifications)):
			frappe.throw(_("Parameter must be unique"))

	def validate(self):
		self.validate_item_specification_line()
		super().validate()
