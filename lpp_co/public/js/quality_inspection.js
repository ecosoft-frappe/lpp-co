// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Quality Inspection", {
	setup: function(frm) {
		var original_set_query_item_code = frm.fields_dict["item_code"].get_query;
		frm.set_query("item_code", function (doc) {
			if (doc.reference_type === "Work Order") {
				if (doc.reference_name) {
					return {
						query: "lpp_co.api.get_work_order_item",
						filters: {reference_type: doc.reference_type, reference_name: doc.reference_name},
					}
				}
			} else {
				return original_set_query_item_code(doc);
			}
		});
	},
	reference_name: function(frm) {
		if (frm.doc.reference_type === "Work Order" && frm.doc.reference_name) {
			frappe.db.get_value("Work Order", {"name": frm.doc.reference_name}, "production_item", (r) => {
				frm.set_value("item_code", r.production_item);
			})
		}
	}
})
