# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
from frappe import _


class SalesOrderLPP(SalesOrder):
	def before_validate(self):
		items = frappe.db.sql_list(
			"""
				select parent
				from `tabItem Customer Detail`
				where parenttype = 'Item' and parentfield = 'customer_items' and customer_name = '{}'
			""".format(self.customer or "")
		)
		for line in self.items:
			if line.item_code not in items:
				frappe.throw(_("Items don't match with the customer, please select new items."))
