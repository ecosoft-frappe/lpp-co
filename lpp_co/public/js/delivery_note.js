// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Delivery Note", {

	refresh(frm) {
		if (
			!frm.doc.is_return &&
			(frm.doc.status != "Closed" || frm.is_new()) &&
			frm.has_perm("write") &&
			frappe.model.can_read("Sales Order") &&
			frm.doc.docstatus === 0
		) {
			setTimeout(() => {
				frm.remove_custom_button(__("Sales Order"), __("Get Items From"))
				frm.add_custom_button(
					__("Sales Order"),
					function () {
						if (!frm.doc.customer) {
							frappe.throw({
								title: __("Mandatory"),
								message: __("Please Select a Customer"),
							});
						}
						erpnext.utils.map_current_doc({
							method: "lpp_co.custom.sales_order.make_delivery_note",
							args: {
								for_reserved_stock: 1,
							},
							source_doctype: "Sales Order",
							target: frm,
							setters: {
								customer: frm.doc.customer,
							},
							get_query_filters: {
								docstatus: 1,
								status: ["not in", ["Closed", "On Hold"]],
								per_delivered: ["<", 99.99],
								company: frm.doc.company,
								project: frm.doc.project || undefined,
							},
							// Monkey Patch
							allow_child_item_selection: true,
							child_fieldname: "items",
							child_columns: ["item_code", "custom_customer_part_no", "item_name", "custom_po_no",  "custom_po_date", "delivery_date", "qty", "delivered_qty", "custom_balance_qty"],
							// -- Monkey Patch
						});
					},
					__("Get Items From")
				);
			}, 500);
		}
	}
});
