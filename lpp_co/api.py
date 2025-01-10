# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe


@frappe.whitelist()
def get_work_order_item(doctype, txt, searchfield, start, page_len, filters):
	doc = frappe.get_doc(filters["reference_type"], filters["reference_name"])
	return [(doc.production_item,)]
