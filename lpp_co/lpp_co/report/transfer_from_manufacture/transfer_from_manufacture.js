// Copyright (c) 2025, Ecosoft and contributors
// For license information, please see license.txt

frappe.query_reports["Transfer From Manufacture"] = {
	"filters": [
		{
			"fieldname": "document",
			"fieldtype": "Data",
			"label": "Document",
			"mandatory": 1,
			"wildcard_filter": 0
		}
	]
};
