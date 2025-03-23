import json
import frappe


@frappe.whitelist()
def check_item_quality_inspection(doctype, items):
	if isinstance(items, str):
		items = json.loads(items)

	inspection_fieldname_map = {
		# "Purchase Receipt": "inspection_required_before_purchase",   # kittiu: Remove checking here
		"Purchase Invoice": "inspection_required_before_purchase",
		"Subcontracting Receipt": "inspection_required_before_purchase",
		"Sales Invoice": "inspection_required_before_delivery",
		"Delivery Note": "inspection_required_before_delivery",
	}

	items_to_remove = []
	for item in items:
		if not frappe.db.get_value("Item", item.get("item_code"), inspection_fieldname_map.get(doctype)):
			items_to_remove.append(item)
	items = [item for item in items if item not in items_to_remove]

	return items
