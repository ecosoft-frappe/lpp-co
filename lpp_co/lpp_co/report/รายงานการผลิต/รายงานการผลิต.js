// Copyright (c) 2025, Ecosoft and contributors
// For license information, please see license.txt

frappe.query_reports["รายงานการผลิต"] = {
	filters: [
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
		{
            label: __("From Posting Date"),
            fieldname: "from_date",
            fieldtype: "Datetime",
            default: (() => {
                const now = frappe.datetime.now_datetime();
                const today_date = now.substr(0, 10);
                const hour = parseInt(now.substr(11, 2));
                let to_date_str = "";
                if (hour >= 8) {
                    to_date_str = today_date + " 08:00:00";
                } else {
                    to_date_str = frappe.datetime.add_days(today_date, -1) + " 08:00:00";
                }
                const from_date_only = frappe.datetime.add_days(to_date_str.substr(0, 10), -1);
                return from_date_only + " 08:00:00";
            })(),
            reqd: 1,
        },
		{
			label: __("To Posting Date"),
			fieldname: "to_date",
			fieldtype: "Datetime",
			default: (() => {
				const now = frappe.datetime.now_datetime(); 
				const today_date = now.substr(0, 10);       
				const hour = parseInt(now.substr(11, 2));
				if (hour >= 8) {
					return today_date + " 08:00:00";
				} else {
					const yesterday = frappe.datetime.add_days(today_date, -1);
					return yesterday + " 08:00:00";
				}
			})(),
			reqd: 1,
		},
	],
};
