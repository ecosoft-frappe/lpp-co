frappe.listview_settings["Quality Inspection Result"] = {
	hide_name_column: true,
    onload: function (listview) {
        // Hide the sidebar when the list view loads
        const sidebar = listview.page.sidebar;
        if (sidebar) {
            sidebar.hide(); // Hide the sidebar
        }
    }
};
