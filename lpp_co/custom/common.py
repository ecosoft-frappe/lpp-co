import frappe
from frappe import _

def validate_child_cost_centers(doc, method):
	"""
	Validate and synchronize cost centers between the document header and line items.
	"""
	head_cost_center = "cost_center"
	if "custom_cost_center" in doc.as_dict():
		head_cost_center = "custom_cost_center"
	if doc.get(head_cost_center):
		for item in doc.items:
			item.cost_center = doc.get(head_cost_center)
	else:
		cost_centers = set(item.cost_center for item in doc.items)
		if len(cost_centers) == 0:
			return
		if len(cost_centers) == 1:
			doc.set(head_cost_center, cost_centers.pop())
		else:
			frappe.msgprint(_("Different cost centers found in line items: {0}. Please ensure consistency.").format(", ".join(cost_centers)))

