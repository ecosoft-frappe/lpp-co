frappe.listview_settings["Stock Entry"] = {
	onload: function(listview) {
		listview.page.add_action_item(__("Run Transfer From Manufacture Report"), function() {
			var selected = listview.get_checked_items();
			if (selected.length === 0) {
				frappe.msgprint(__("Please select at least one Stock Entry"));
				return;
			}

			var names = selected.map(doc => doc.name);

			frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Stock Entry",
					filters: { name: ["in", names] },
					fields: ["posting_date", "custom_cost_center", "stock_entry_type"]
				},
				callback: function(response) {
					if (response.message) {
						var entries = response.message;

						var invalid_types = entries.filter(entry => entry.stock_entry_type !== "Manufacture");
						if (invalid_types.length > 0) {
							frappe.msgprint(__("Selected Stock Entry must have type 'Manufacture'."));
							return;
						}

						// var unique_post_dates = [...new Set(entries.map(entry => entry.posting_date))];
						// var unique_cost_centers = [...new Set(entries.map(entry => entry.custom_cost_center))];

						// if (unique_post_dates.length > 1 || unique_cost_centers.length > 1) {
						// 	frappe.msgprint(__("Selected Stock Entry must have the same Posting Date and Cost Center."));
						// 	return;
						// }

						frappe.set_route("query-report", "Transfer From Manufacture", {
							"document": names.join(",")
						});
					}
				}
			});
		});
	}
};
