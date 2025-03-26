// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sales Invoice", {
    refresh(frm) {
		if (frm.doc.docstatus === 0) {
			setTimeout(() => {
				frm.remove_custom_button(__("Sales Order"), __("Get Items From"))
				frm.add_custom_button(
					__("Sales Order"),
					function () {
						erpnext.utils.map_current_doc({
							method: "lpp_co.custom.sales_order.make_sales_invoice",
							source_doctype: "Sales Order",
							target: frm,
							setters: {
								customer: frm.doc.customer || undefined,
								po_no: frm.doc.po_no || undefined,
							},
							get_query_filters: {
								docstatus: 1,
								status: ["not in", ["Closed", "On Hold"]],
								per_billed: ["<", 99.99],
								company: frm.doc.company,
							},
							// Monkey Patch
							allow_child_item_selection: true,
							child_fieldname: "items",
							child_columns: ["custom_customer_part_no", "item_name", "custom_po_no",  "custom_po_date", "delivery_date", "qty", "delivered_qty", "custom_balance_qty"],
							// -- Monkey Patch
						});
					},
					__("Get Items From")
				);
			}, 1000);
		}
    },
});
