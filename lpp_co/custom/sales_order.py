# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.selling.doctype.sales_order.sales_order import (
    SalesOrder,
    make_material_request as original_make_material_request
)


class SalesOrderLPP(SalesOrder):
	def before_validate(self):
		items = frappe.db.sql_list(
			"""
				select parent
				from `tabItem Customer Detail`
				where parenttype = 'Item' and parentfield = 'customer_items' and customer_name = '{}'
			""".format(self.customer or "")
		)
		for line in self.items:
			if line.item_code not in items:
				frappe.throw(_("Items don't match with the customer, please select new items."))


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
