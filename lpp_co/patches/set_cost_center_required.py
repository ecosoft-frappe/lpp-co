from lpp_co.hooks import cost_center_field_doctypes
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def execute():
	for doctype in cost_center_field_doctypes:
		make_property_setter(doctype, "cost_center", "reqd", 1, "Check")
