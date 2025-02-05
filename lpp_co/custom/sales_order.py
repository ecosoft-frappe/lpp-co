# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.selling.doctype.sales_order.sales_order import (
    make_material_request as original_make_material_request,
    make_sales_invoice as original_make_sales_invoice,
)


def update_sales_order_item(doc, method):
    # Update po_no field, into all sales order items
    frappe.db.set_value(
		"Sales Order Item",
		{"parent": doc.name},
		"custom_po_no",
		doc.po_no,
		update_modified=False,
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


@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None, args=None):
	if args == None:
		args = {}
	doc = original_make_sales_invoice(source_name, target_doc)
	if args.get("filtered_children"):
		for d in doc.items:
			doc.items = list(filter(lambda d: d.so_detail in args["filtered_children"], doc.items))
	return doc
