// Hide timer buttons
frappe.ui.form.off("Job Card", "prepare_timer_buttons");


frappe.ui.form.on("Job Card", {
	async refresh(frm) {
		// Fetch all items in a BOM
		if (frm.doc.bom_no) {
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
		
		frappe.db.get_value("Item", frm.doc.production_item, "custom_item_group_2", (r) => {
			["custom_job_card_defect_1", "custom_job_card_defect_2", "custom_job_card_defect_2"].forEach(field => {
				frm.set_query("defect", field, () => {
					return {
						query: "lpp_co.custom.common.qi_params_query",
						filters: {
							item_group: r.custom_item_group_2,
							custom_is_item_spec: 0
						},
					};
				});
			});
		})
	}
});

// frappe.ui.form.on("Job Card Time Loss", {
//     from_time: function(frm, cdt, cdn) {
//         calculate_time_loss_minutes(frm, cdt, cdn);
//     },
//     to_time: function(frm, cdt, cdn) {
//         calculate_time_loss_minutes(frm, cdt, cdn);
//     }
// });

// function calculate_time_loss_minutes(frm, cdt, cdn) {
//     let child = locals[cdt][cdn];
//     if (child.from_time && child.to_time) {
//         let from_time = new Date(`1970-01-01T${child.from_time}Z`);
//         let to_time = new Date(`1970-01-01T${child.to_time}Z`);
//         let diff = (to_time - from_time) / (1000 * 60); // Difference in minutes
// 		frappe.model.set_value(cdt, cdn, 'minutes', diff);
//     } else {
// 		frappe.model.set_value(cdt, cdn, 'minutes', '');
// 	}
// }
