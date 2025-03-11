import frappe


def set_print_format_as_disable():
	print_formats = [
		"Sales Order PD v2",
		"Drop Shipping Format",
		"Bank and Cash Payment Voucher",
	]
	for print_format in print_formats:
		frappe.db.set_value("Print Format", print_format, "disabled", 1)
