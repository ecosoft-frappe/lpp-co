// Hide timer buttons
frappe.ui.form.off("Job Card", "prepare_timer_buttons");


frappe.ui.form.on("Job Card", {
	async refresh(frm) {
		// Fetch all items in a BOM
		let r = await frappe.call({
			method: "lpp_co.custom.job_card.get_bom_items",
			args: {
				bom: frm.doc.bom_no
			}
		});
		frm.fields_dict["scrap_items"].grid.get_field("item_code").get_query = function() {
			return {
				query: "erpnext.controllers.queries.item_query",
				filters: {
					name: ["in", r.message]
				}
			};
		}
	}
});