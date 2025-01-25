# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import (
    make_purchase_invoice as original_make_purchase_invoice
)
from frappe import _


@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None, args=None):
	doclist = original_make_purchase_invoice(source_name, target_doc, args)
	doc_receipt = frappe.get_doc("Purchase Receipt", source_name)
	doclist.bill_no = doc_receipt.custom_supplier_invoice_number
	doclist.bill_date = doc_receipt.custom_supplier_invoice_date
	return doclist
