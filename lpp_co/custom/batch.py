# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.naming import make_autoname
from erpnext.stock.doctype.batch.batch import Batch

class BatchLPP(Batch):

	@property
	def customer_item(self):
		item = frappe.get_doc("Item", self.item)
		customer = frappe.get_value("Customer", {"customer_name": self.custom_customer_name})
		if item.customer_items and customer:
			customer_item = list(filter(lambda l: l.customer_name == customer, item.customer_items))
			if customer_item:
				return customer_item[0]
		return None

	@property
	def item_doc(self):
		item = frappe.get_doc("Item", self.item)
		return item

	@property
	def workorder_doc(self):
		if self.reference_doctype == "Work Order" and self.reference_name:
			work_order = frappe.get_doc("Work Order", self.reference_name)
			return work_order
		return None

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
		if self.custom_rescreen:
			self.name += "-R"
		self.batch_id = self.name
		# Validate if batch_id is unique
		if frappe.db.exists("Batch", self.name):
			frappe.throw(_("Batch ID {0} already exists").format(self.name))

	def before_insert(self):
		# Make sure customer name is updated
		if not self.custom_customer_name:
			if self.reference_doctype == "Work Order" and self.reference_name:
				work_order = frappe.get_doc("Work Order", self.reference_name)
				self.custom_customer_name = work_order.custom_customer_name
			elif self.item:
				item = frappe.get_doc("Item", self.item)
				if len(item.customer_items) > 0 and item.customer_items[0].customer_name:
					customer = frappe.get_doc("Customer", item.customer_items[0].customer_name)
					self.custom_customer_name = customer.customer_name
				else:
					self.custom_customer_name = ""
			else:
				self.custom_customer_name = ""
