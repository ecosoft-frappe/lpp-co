// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt
frappe.ui.form.on('Stock Entry Detail', {
    is_finished_item: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.is_finished_item) {
            frappe.model.set_value(cdt, cdn, 's_warehouse', null);
        }
    }
});