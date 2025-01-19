// Copyright (c) 2025, Ecosoft and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Quality Inspection Result", {
// 	refresh(frm) {

// 	},
// });

// Event handler for the child table
frappe.ui.form.on("Quality Inspection Result Reading", {
	reading: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		let max = frm.doc.nominal + frm.doc.delta_plus;
		let min = frm.doc.nominal - frm.doc.delta_minus;
		if (min <= row.reading && row.reading <= max) {
			frappe.model.set_value(cdt, cdn, "result", "Accepted");
		} else {
			frappe.model.set_value(cdt, cdn, "result", "Rejected");
		}
	}
});