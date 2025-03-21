# Copyright (c) 2025, Ecosoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data, None, None, None


def get_columns():
	return [
		{
			"fieldname": "stock_entry",
			"fieldtype": "Link",
			"label": "Document No.",
			"options": "Stock Entry",
			"width": 0
		},
		{
			"fieldname": "item_code",
			"fieldtype": "Data",
			"label": "Item Code",
			"width": 0
		},
		{
			"fieldname": "item_name",
			"fieldtype": "Data",
			"label": "Item Name",
			"width": 0
		},
		{
			"fieldname": "work_order",
			"fieldtype": "Link",
			"label": "Work Order",
			"options": "Work Order",
			"width": 0
		},
		{
			"fieldname": "batch_no",
			"fieldtype": "Link",
			"label": "Batch No.",
			"options": "Batch",
			"width": 0
		},
		{
			"fieldname": "unit_pack",
			"fieldtype": "Int",
			"label": "Unit / Pack",
			"width": 0
		},
		{
			"fieldname": "unit_box",
			"fieldtype": "Int",
			"label": "Unit / Box",
			"width": 0
		},
		{
			"fieldname": "count",
			"fieldtype": "Int",
			"label": "Count",
			"width": 0
		},
		{
			"fieldname": "qty",
			"fieldtype": "Float",
			"label": "Quantity",
			"width": 0
		},
		{
			"fieldname": "t_warehose",
			"fieldtype": "Link",
			"label": "Target WH",
			"options": "Warehouse",
			"width": 0
		}
	]


def get_data(filters):
	result = frappe.db.sql(
		"""
			select
				se.name as stock_entry,
				sed.item_code,
				sed.item_name,
				se.work_order,
				sed.batch_no,
				i.custom_unit_pack as unit_pack,
				i.custom_unit_box as unit_box,
				case
					when i.custom_unit_box then floor(sed.qty / i.custom_unit_box)
					when i.custom_unit_pack then floor(sed.qty / i.custom_unit_pack)
					else 0
				end as count,
				sed.qty,
				sed.t_warehouse,
				se.posting_date,
				se.custom_cost_center,
				c.company_logo,
				c.custom_company_name_en,
				c.custom_company_name_th
			from `tabStock Entry Detail` sed
			left join `tabStock Entry` se on sed.parent = se.name
			left join `tabItem` i on sed.item_code = i.name
			left join `tabCompany` c on se.company = c.name
			where se.stock_entry_type = "Manufacture" and se.name in %(documents)s
			order by se.name, sed.item_code
		""", {"documents": tuple(filters["document"].split(","))},
		as_dict=True
	)
	return result
