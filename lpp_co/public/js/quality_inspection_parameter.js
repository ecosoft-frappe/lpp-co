// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Quality Inspection Parameter", {
	onload(frm) {
	    // Filter Item Group Level 2, all have All Item Groups as grand pa
		frm.set_query("custom_related_item_groups", () => {
			return {
				filters: {
					custom_grand_parent_item_group: "All Item Groups",
				},
			};
		});
	}
})