# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def validate_customer_item(doc, method):
	if doc._action != "save":
		return
	for line in doc.items:
		item = frappe.get_cached_doc("Item", line.item_code)
		if not item.customer_items:
			continue
		customers = [x.customer_name for x in item.customer_items]
		customer = doc.get("party_name") or doc.get("customer") or ""
		if customer not in customers:
			frappe.msgprint(
				_("Item {} does not belong to customer {}.".format(line.item_code, customer))
			)
