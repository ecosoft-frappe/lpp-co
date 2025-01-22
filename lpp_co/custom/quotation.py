# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from erpnext.selling.doctype.quotation.quotation import Quotation
from frappe import _


class QuotationLPP(Quotation):
    pass
	# def before_validate(self):
	# 	if self.quotation_to == "Customer":
	# 		items = frappe.db.sql_list(
	# 			"""
	# 				select parent
	# 				from `tabItem Customer Detail`
	# 				where parenttype = 'Item' and parentfield = 'customer_items' and customer_name = '{}'
	# 			""".format(self.party_name or "")
	# 		)
	# 		for line in self.items:
	# 			if line.item_code not in items:
	# 				frappe.throw(_("Items don't match with the customer, please select new items."))


@frappe.whitelist()
def get_quotation_item(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(
		"""
			select i.name, i.item_name
			from `tabItem Customer Detail` icd
			join `tabItem` i on icd.parent = i.name
			where icd.parenttype = 'Item' and icd.parentfield = 'customer_items' and icd.customer_name = '{}'
		""".format(
			filters.get("customer_name", ""),
		)
	)
