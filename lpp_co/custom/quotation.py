# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from erpnext.selling.doctype.quotation.quotation import Quotation
from frappe import _


class QuotationLPP(Quotation):
	def before_validate(self):
		if self.quotation_to == "Customer":
			items = frappe.db.sql_list(
				"""
					select parent
					from `tabItem Customer Detail`
					where parenttype = 'Item' and parentfield = 'customer_items' and customer_name = '{}'
				""".format(self.party_name or "")
			)
			for line in self.items:
				if line.item_code not in items:
					frappe.throw(_("Items don't match with the customer, please select new items."))
