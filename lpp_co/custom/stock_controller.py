import json
import frappe
from frappe.utils import flt
from frappe import _


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


@frappe.whitelist()
def make_quality_inspections(doctype, docname, items):
	if isinstance(items, str):
		items = json.loads(items)

	inspections = []
	for item in items:
		if flt(item.get("sample_size")) > flt(item.get("qty")):
			frappe.throw(
				_(
					"{item_name}'s Sample Size ({sample_size}) cannot be greater than the Accepted Quantity ({accepted_quantity})"
				).format(
					item_name=item.get("item_name"),
					sample_size=item.get("sample_size"),
					accepted_quantity=item.get("qty"),
				)
			)
		# If doctype == "Purchase Receipt" and on line item has serial_and_batch_bundle
		# Find all batch_no in Serial and Batch Bundle and create quality inspection for each batch_no
		# Else create quality inspection for the line item
		batch_nos = []
		if doctype == "Purchase Receipt" and item.get("child_row_reference"):
			srb = frappe.db.get_value("Purchase Receipt Item", item.get("child_row_reference"), "serial_and_batch_bundle")
			if srb:
				bundle = frappe.get_doc("Serial and Batch Bundle", srb)
				batch_nos = [l.batch_no for l in bundle.entries]
		qi = {
			"doctype": "Quality Inspection",
			"inspection_type": "Incoming",
			"inspected_by": frappe.session.user,
			"reference_type": doctype,
			"reference_name": docname,
			"item_code": item.get("item_code"),
			"description": item.get("description"),
			"sample_size": flt(item.get("sample_size")),
			"item_serial_no": item.get("serial_no").split("\n")[0] if item.get("serial_no") else None,
			"batch_no": item.get("batch_no"),
			"custom_qc_quantity": flt(item.get("custom_qc_quantity", 0)),
            "custom_qc_uom": item.get("custom_qc_uom", "")
		}
		if not batch_nos:
			# Original
			quality_inspection = frappe.get_doc(qi).insert()
			quality_inspection.save()
			inspections.append(quality_inspection.name)
		else:
			# Extended
			for batch_no in batch_nos:
				qi["batch_no"] = batch_no  # Change to batch from the bundle
				quality_inspection = frappe.get_doc(qi).insert()
				quality_inspection.save()
				inspections.append(quality_inspection.name)

	return inspections
