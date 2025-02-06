// Copyright (c) 2025, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Quality Inspection Result", {
    onload: function(frm) {
		frm.set_df_property("readings", "cannot_add_rows", true);
		frm.set_df_property("readings", "cannot_delete_rows", true);
    }
});

// Event handler for the child table
frappe.ui.form.on("Quality Inspection Result Reading", {
	reading: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (allNumbers([frm.doc.nominal, frm.doc.delta_minus, frm.doc.delta_plus, row.reading])) {
			let max = parseFloat(frm.doc.nominal) + parseFloat(frm.doc.delta_plus);
			let min = parseFloat(frm.doc.nominal) - parseFloat(frm.doc.delta_minus);
			let reading = parseFloat(row.reading);
			if (min <= reading && reading <= max) {
				frappe.model.set_value(cdt, cdn, "result", "Accepted");
			} else {
				frappe.model.set_value(cdt, cdn, "result", "Rejected");
			}
		}
	}
});

function allNumbers(values) {
    for (let i = 0; i < values.length; i++) {
        let floatValue = parseFloat(values[i]);
        if (isNaN(floatValue) || floatValue.toString() !== values[i].trim()) {
            return false;
        }
    }
    return true;
}
