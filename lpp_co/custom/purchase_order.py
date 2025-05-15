import frappe
from frappe.utils import flt
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


def set_balance_qty(doc, method):
	names = []
	if doc.doctype in ["Purchase Invoice", "Purchase Receipt"]:
		names = list(set([item.purchase_order for item in doc.items if item.purchase_order]))
	if doc.doctype == "Purchase Order":
		names = [doc.name]
	for name in names:
		doc = frappe.get_doc("Purchase Order", name)
		for item in doc.items:
			frappe.db.set_value("Purchase Order Item", item.name, "custom_balance_qty", flt(item.qty - item.received_qty), update_modified=False)
