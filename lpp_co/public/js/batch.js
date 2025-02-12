frappe.ui.form.on("Batch", {
	reference_name: function(frm) {
		update_customer_name(frm);
	},
	item: function(frm) {
		update_customer_name(frm);
	}
});

function update_customer_name(frm) {
	if (frm.doc.reference_doctype == "Work Order" && frm.doc.reference_name) {
		frappe.db.get_doc("Work Order", frm.doc.reference_name).then((doc) => {
			frm.set_value("custom_customer_name", doc.custom_customer_name);
		})
	} else if (frm.doc.item) {
		frappe.db.get_doc("Item", frm.doc.item).then((doc) => {
			if (doc.customer_items.length > 0 && doc.customer_items[0].customer_name) {
				frappe.db.get_doc("Customer", doc.customer_items[0].customer_name).then((cust) => {
					frm.set_value("custom_customer_name", cust.customer_name);
				})
			} else {
				frm.set_value("custom_customer_name", "");
			}
		});
	} else {
		frm.set_value("custom_customer_name", "");
	}
}
