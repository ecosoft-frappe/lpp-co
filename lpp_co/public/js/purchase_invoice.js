// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Purchase Invoice", {
	refresh(frm) {
		if (frm.doc.docstatus === 0) {
			setTimeout(() => {
				frm.remove_custom_button(__("Purchase Receipt"), __("Get Items From"))
				frm.add_custom_button(
					__("Purchase Receipt"),
					function () {
						erpnext.utils.map_current_doc({
							method: "lpp_co.custom.purchase_receipt.make_purchase_invoice",
							source_doctype: "Purchase Receipt",
							target: frm,
							setters: {
								supplier: frm.doc.supplier || undefined,
								posting_date: undefined,
							},
							get_query_filters: {
								docstatus: 1,
								status: ["not in", ["Closed", "Completed", "Return Issued"]],
								company: frm.doc.company,
								is_return: 0,
							},
						});
					},
					__("Get Items From")
				);
			}, 500);
		}
    },
});
