// Hide timer buttons
frappe.ui.form.off("Job Card", "prepare_timer_buttons");

frappe.ui.form.on("Job Card", {
	refresh: function (frm) {
        // Set query for item_code field in Job Card Scrap Item child table
        frm.fields_dict["scrap_items"].grid.get_field("item_code").get_query = function(doc, cdt, cdn) {
            let child = locals[cdt][cdn];
            return {
                query: "lpp_co.custom.job_card.get_bom_items",
                filters: {
                    bom: frm.doc.bom_no
                }
            };
        };
	}
});