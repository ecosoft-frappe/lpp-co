# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe


@frappe.whitelist()
def get_work_order_item(doctype, txt, searchfield, start, page_len, filters):
	doc = frappe.get_doc(filters["reference_type"], filters["reference_name"])
	return [(doc.production_item,)]


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


@frappe.whitelist()
def get_sale_order_item(doctype, txt, searchfield, start, page_len, filters):
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
