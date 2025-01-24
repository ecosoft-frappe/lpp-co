# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.selling.doctype.sales_order.sales_order import (
    make_material_request as original_make_material_request
)


@frappe.whitelist()
def make_material_request(source_name, target_doc=None):
	doc = original_make_material_request(source_name, target_doc)
	# Adding more data to the Material Request
	for d in doc.items:
		if d.sales_order:
			so = frappe.get_doc("Sales Order", d.sales_order)
			d.schedule_date = so.delivery_date
	# --
	return doc
