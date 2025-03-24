import frappe


def set_print_format_as_disable():
	print_formats = [
		"Sales Order PD v2",
		"Drop Shipping Format",
		"Bank and Cash Payment Voucher",
		"Purchase Auditing Voucher",
		"Sales Auditing Voucher",
		"Sales Invoice Return",
		"Point of Sale",
		"Sales Invoice PD Format v2",
		"Sales Invoice Print",
		"Purchase Receipt Serial and Batch Bundle Print",
	]
	for print_format in print_formats:
		frappe.db.set_value("Print Format", print_format, "disabled", 1)
