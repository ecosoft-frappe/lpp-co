# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import get_ancestors_of
from frappe import _


@frappe.whitelist()
def get_item_quality_specification(item_group):
	# Find item specification groups related to this item
	item_groups = get_ancestors_of("Item Group", item_group)
	item_groups.append(item_group)
	params = frappe.get_all(
		"Quality Inspection Parameter",
		filters=[
			["Quality Inspection Parameter Item Group",
				"item_group", "in", item_groups],
			["custom_is_item_spec", "=", 1]
		],
		pluck="name",
		order_by="custom_sequence asc"  
	)
	return list(dict.fromkeys(params))


def validate_item_specification_line(doc, method):
	# Validate unique parameter in the item
	specifications = [line.specification for line in doc.custom_item_specification_line]
	if len(specifications) != len(set(specifications)):
		frappe.throw(_("Parameter must be unique"))

def set_field_customer_items(doc, method):
	# This will be used as search field
	row_search = []
	ref_codes = []
	sheet_nos = []
	customers = []
	for row in doc.customer_items:
		row_search.append(
			" ".join([str(row.get(f) or "")
			for f in [
				"customer_name",
				"custom_drawing_build_sheet_no",
				"ref_code",
				"custom_lpp_part_no"
			]]))
		ref_codes.append(row.ref_code or "")
		sheet_nos.append(row.custom_drawing_build_sheet_no or "")
		if row.customer_name:
			customer = frappe.db.get_value("Customer", row.customer_name, "customer_name")
			customers.append(customer)
	frappe.db.set_value("Item", doc.name, "custom_search_customer_items", ", ".join(row_search) or "")
	frappe.db.set_value("Item", doc.name, "custom_ref_code", ", ".join(ref_codes[:1]) or "")
	frappe.db.set_value("Item", doc.name, "custom_drawing_build_sheet_no", ", ".join(sheet_nos) or "")
	frappe.db.set_value("Item", doc.name, "custom_customer_name", ", ".join(customers) or "")
	doc.reload()
 
