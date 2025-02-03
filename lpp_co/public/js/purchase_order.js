// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Purchase Order", {
    refresh(frm) {
		if (frm.doc.docstatus === 0) {
			setTimeout(() => {
				frm.remove_custom_button(__("Material Request"), __("Get Items From"))
				frm.add_custom_button(
					__("Material Request"),
					function () {
						erpnext.utils.map_current_doc({
							method: "erpnext.stock.doctype.material_request.material_request.make_purchase_order",
							source_doctype: "Material Request",
							target: frm,
							setters: {
								schedule_date: undefined,
							},
							get_query_filters: {
								material_request_type: "Purchase",
								docstatus: 1,
								status: ["!=", "Stopped"],
								per_ordered: ["<", 100],
								company: frm.doc.company,
							},
							allow_child_item_selection: true,
							child_fieldname: "items",
							child_columns: ["item_code", "item_name", "qty", "ordered_qty"],
						});
					},
					__("Get Items From")
				);
			}, 500);
		}
    },
});
