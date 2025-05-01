import frappe
from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt as origin_make_purchase_receipt


@frappe.whitelist()
def make_purchase_receipt(source_name, target_doc=None, args=None):
	if args is None:
		args = {}
	doc = origin_make_purchase_receipt(source_name, target_doc=target_doc)
	if args.get("filtered_children"):
		doc.items = list(filter(
			lambda d: d.purchase_order_item in args["filtered_children"], doc.items))
	return doc
