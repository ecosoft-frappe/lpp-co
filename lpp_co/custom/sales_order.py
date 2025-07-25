# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from erpnext.selling.doctype.sales_order.sales_order import (
    make_material_request as original_make_material_request,
    make_sales_invoice as original_make_sales_invoice,
    make_delivery_note as original_make_delivery_note,
)


def update_sales_order_item(doc, method):
    # Update po_no field, into all sales order items
    frappe.db.set_value(
		"Sales Order Item", {"parent": doc.name}, "custom_po_no", doc.po_no, update_modified=False,
	)
    frappe.db.set_value(
		"Sales Order Item", {"parent": doc.name}, "custom_po_date", doc.po_date, update_modified=False,
	)

def set_balance_qty(doc, method):
	names = []
	if doc.doctype == "Sales Invoice":
		names = list(set([item.sales_order for item in doc.items if item.sales_order]))
	if doc.doctype == "Delivery Note":
		names = list(set([item.against_sales_order for item in doc.items if item.against_sales_order]))
	if doc.doctype == "Sales Order":
		names = [doc.name]
	for name in names:
		doc = frappe.get_doc("Sales Order", name)
		for item in doc.items:
			frappe.db.set_value("Sales Order Item", item.name, "custom_balance_qty", flt(item.qty - item.delivered_qty), update_modified=False)

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


@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None, args=None):
	if args == None:
		args = {}
	doc = original_make_delivery_note(source_name, target_doc)
	if args.get("filtered_children"):
		for d in doc.items:
			doc.items = list(filter(lambda d: d.so_detail in args["filtered_children"], doc.items))
	return doc

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_sales_order_not_delivered(doctype, txt, searchfield, start, page_len, filters):
	conditions = ""
	if txt:
		conditions += " and so.name like '%%%s%%'" % (txt, )
	if filters.get("customer"):
		conditions += " and so.customer = '%s'" % (filters["customer"], )
	if filters.get("po_no"):
		conditions += " and so.po_no %s '%%%s%%'" % (filters["po_no"][0], filters["po_no"][1])
	if filters.get("docstatus"):
		conditions += " and so.docstatus = %s" % (filters["docstatus"])
	if filters.get("status"):
		conditions += " and so.status %s %s" % (filters["status"][0], tuple(filters["status"][1]))
	if filters.get("per_billed"):
		conditions += " and so.per_billed %s %s" % (filters["per_billed"][0], filters["per_billed"][1])
	if filters.get("company"):
		conditions += " and so.company = '%s' " % (filters["company"], )
	so_data = frappe.db.sql(
		f"""
			select distinct so.name, so.customer, so.po_no
			from `tabSales Order` so, `tabSales Order Item` soi
			where
				so.name = soi.parent
				and soi.custom_balance_qty > 0
				{conditions}
			-- order by so.name asc
		""",
		as_dict=1
	)
	return so_data
