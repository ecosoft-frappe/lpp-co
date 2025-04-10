import frappe


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
		if len(cost_centers) == 1:
			doc.set(head_cost_center, cost_centers.pop())
		else:
			doc.set(head_cost_center, "")


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def qi_params_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(
		"""select parent from `tabQuality Inspection Parameter Item Group`
		where item_group = {}
		and parent not in (select name from `tabQuality Inspection Parameter` where custom_is_item_spec = 1)
		and parent like {} order by name limit {} offset {}""".format("%s", "%s", "%s", "%s"),
		(filters["item_group"], "%%%s%%" % txt, page_len, start),
		as_list=1,
	)