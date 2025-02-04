# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.naming import make_autoname
from erpnext.stock.doctype.batch.batch import Batch

class BatchLPP(Batch):

	def autoname(self):
		super().autoname()
		item = frappe.get_cached_doc("Item", self.item)
		suffix = ""
		if item.custom_batch_suffix:
			item_groups = {
				"Item Group 1 Abbr": "custom_item_group_1",
				"Item Group 2 Abbr": "custom_item_group_2",
				"Item Group 3 Abbr": "item_group",
			}
			if item.custom_batch_suffix in item_groups.keys():
				suffix = frappe.get_value(
        			"Item Group",
           			item.get(item_groups[item.custom_batch_suffix]),
              		"custom_abbreviation"
            	)
		if suffix:
			self.name += f"-{suffix}"