frappe.listview_settings['Item'] = {
	onload: function(listview) {
		if (listview.page.fields_dict.custom_item_tag_1) {
			listview.page.fields_dict.custom_item_tag_1.get_query = function() {
				return { "filters": { "level_1": ["=", 1] } };
			};
		}
		if (listview.page.fields_dict.custom_item_tag_2) {
			listview.page.fields_dict.custom_item_tag_2.get_query = function() {
				return { "filters": { "level_2": ["=", 1] } };
			};
		}
		if (listview.page.fields_dict.custom_item_tag_3) {
			listview.page.fields_dict.custom_item_tag_3.get_query = function() {
				return { "filters": { "level_3": ["=", 1] } };
			};
		}
	}
}