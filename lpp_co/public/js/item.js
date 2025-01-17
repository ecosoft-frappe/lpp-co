frappe.ui.form.on("Item", {
    custom_reset_quality_parameters: function(frm) {
        frappe.call({
            method: "get_item_quality_specification",
			doc: frm.doc,
            callback: function(r) {
                if(r.message) {
                    // Assuming r.message is an array of parameters
					frm.clear_table('custom_item_specification_line');
                    r.message.forEach(param => {
                        let new_row = frm.add_child("custom_item_specification_line");
                        new_row.specification = param;
                    });
                    frm.refresh_field("custom_item_specification_line");
                }
            }
        });
    }
})