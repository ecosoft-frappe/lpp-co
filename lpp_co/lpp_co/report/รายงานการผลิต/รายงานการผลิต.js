// Copyright (c) 2025, Ecosoft and contributors
// For license information, please see license.txt

frappe.query_reports["รายงานการผลิต"] = {
	filters: [
		{
			label: __("From Posting Date"),
			fieldname: "from_date",
			fieldtype: "Datetime",
			default: frappe.datetime.month_start(frappe.datetime.get_today()) + " 00:00:00",
			reqd: 1,
		},
		{
			label: __("To Posting Date"),
			fieldname: "to_date",
			fieldtype: "Datetime",
			default: frappe.datetime.month_end(frappe.datetime.get_today()) + " 00:00:00",
			reqd: 1,
		},		
		{
			label: __("Status"),
			fieldname: "status",
			fieldtype: "Select",
			options: ["", "Open", "Work In Progress", "Completed", "On Hold"],
		},
		{
			label: __("Work Orders"),
			fieldname: "work_order",
			fieldtype: "MultiSelectList",
			options: "Work Order",
			get_data: function (txt) {
				return frappe.db.get_link_options("Work Order", txt);
			},
		},
		{
			label: __("Operation"),
			fieldname: "operation",
			fieldtype: "Link",
			options: "Operation",
		},
		{
			label: __("Workstation"),
			fieldname: "workstation",
			fieldtype: "Link",
			options: "Workstation",
		},
		{
			label: __("Workstation Type"),
			fieldname: "workstation_type",
			fieldtype: "Link",
			options: "Workstation Type",
		},
		{
			label: __("Production Item"),
			fieldname: "production_item",
			fieldtype: "MultiSelectList",
			options: "Item",
			get_data: function (txt) {
				return frappe.db.get_link_options("Item", txt);
			},
		},
	],
};
