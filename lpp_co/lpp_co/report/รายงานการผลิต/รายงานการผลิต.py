# Copyright (c) 2025, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, flt

from erpnext.stock.report.stock_analytics.stock_analytics import get_period, get_period_date_ranges


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    chart_data = get_chart_data(data, filters)
    total_row = calculate_totals(data)
    if total_row:
        data.append(total_row)

    return columns, data, None, chart_data

def get_data(filters):
    job_cards = get_job_cards(filters)
    if not job_cards:
        return []

    job_card_names = [jc.name for jc in job_cards]
    time_logs = get_time_logs(job_card_names, filters)
    time_log_map = group_by_parent(time_logs)
    employee_map = get_employee_map(time_logs)

    result = []
    for jc in job_cards:
        logs = time_log_map.get(jc.name, [])
        for i, log in enumerate(logs, 1):
            result += build_rows(jc, log, i, employee_map)
    return result

def get_job_cards(filters):
    query_filters = {"docstatus": ("<", 2)}
    for f in ["work_order", "production_item"]:
        if filters.get(f):
            query_filters[f] = ("in", filters[f])
    for f in ["workstation", "operation", "status", "company", "workstation_type"]:
        if filters.get(f):
            query_filters[f] = filters[f]

    fields = [
        "name", "status", "work_order", "production_item", "item_name", "posting_date",
        "total_completed_qty", "workstation", "operation", "total_time_in_mins",
        "custom_job_card_name", "workstation_type", "for_quantity",
        "custom_total_input_qty", "custom_scrap_qty", "custom_yield",
        "custom_total_setup_defect_qty", "custom_yield_setup"
    ]
    return frappe.get_all("Job Card", fields=fields, filters=query_filters)

def get_time_logs(job_card_names, filters):
    tl_filters = {"parent": ["in", job_card_names]}
    if filters.get("from_date"):
        tl_filters["from_time"] = (">=", filters["from_date"])
    if filters.get("to_date"):
        tl_filters["to_time"] = ("<=", filters["to_date"])

    return frappe.get_all(
        "Job Card Time Log",
        fields=[
            "name", "parent", "from_time", "to_time", "custom_type", "custom_shift",
            "employee", "completed_qty", "custom_input_qty", "time_in_mins", "custom_units_hour_log"
        ],
        filters=tl_filters,
        order_by="idx asc"
    )

def get_employee_map(time_logs):
    employee_ids = list({log["employee"] for log in time_logs if log.get("employee")})
    if not employee_ids:
        return {}
    employees = frappe.get_all("Employee", fields=["name", "employee_name"], filters={"name": ["in", employee_ids]})
    return {e.name: e.employee_name for e in employees}

def group_by_parent(items):
    result = {}
    for item in items:
        result.setdefault(item["parent"], []).append(item)
    return result

def build_rows(jc, log, sequence, employee_map):
    completed_qty = flt(log.get("completed_qty") or 0)
    time_in_mins = flt(log.get("time_in_mins") or 0)
    log["custom_units_hour_log"] = round((completed_qty / time_in_mins) * 60, 2) if time_in_mins else 0

    employee_name = employee_map.get(log["employee"], log["employee"])
    parentfield = f"custom_job_card_defect_{sequence}"
    defects = frappe.get_all(
        "Job Card Defect",
        fields=["defect", "qty"],
        filters={"parent": jc.name, "parentfield": parentfield}
    )

    base_row = jc.copy()
    add_common_fields(base_row, log, sequence, employee_name, jc)

    fields_to_blank = [
        "for_quantity", "custom_total_input_qty", "total_completed_qty", "custom_scrap_qty", "custom_yield",
        "custom_total_setup_defect_qty", "custom_yield_setup", "total_time_in_mins", "custom_unit_hours"
    ]

    rows = []

    if defects:
        first = True
        for defect in defects:
            row = base_row.copy() if first else add_defect_row(jc, fields_to_blank)
            if first:
                first = False
            row.update({"defect": defect.defect, "qty": defect.qty})
            rows.append(row)
    else:
        base_row.update({"defect": "-", "qty": 0})
        rows.append(base_row)

    return rows

def add_common_fields(row, log, sequence, employee_name, jc):
    row.update({
        "sequence": sequence,
        "from_time": log["from_time"],
        "to_time": log["to_time"],
        "custom_type": log["custom_type"],
        "custom_shift": log["custom_shift"],
        "employee": employee_name,
        "completed_qty": log["completed_qty"],
        "custom_input_qty": log["custom_input_qty"],
        "time_in_mins": log["time_in_mins"],
        "custom_units_hour_log": log["custom_units_hour_log"],
        "custom_unit_hours": round((flt(jc.get("total_completed_qty") or 0) / flt(jc.get("total_time_in_mins") or 0)) * 60, 2) if jc.get("total_time_in_mins") else 0
    })

def add_defect_row(jc, fields_to_blank):
    row = {k: jc.get(k, "") for k in [
        "name", "status", "work_order", "production_item", "item_name", "posting_date",
        "workstation", "operation", "custom_job_card_name", "workstation_type"
    ]}
    for k in fields_to_blank:
        row[k] = ""
    return row

def get_chart_data(job_card_details, filters):
    labels, periodic_data = prepare_chart_data(job_card_details, filters)

    datasets = [
        {
            "name": _("Total Input Qty"),
            "values": [periodic_data["custom_total_input_qty"].get(label, 0) for label in labels],
        },
        {
            "name": _("Total Completed Qty"),
            "values": [periodic_data["total_completed_qty"].get(label, 0) for label in labels],
        },
        {
            "name": _("Total Production Defect Qty"),
            "values": [periodic_data["custom_scrap_qty"].get(label, 0) for label in labels],
        },
    ]

    return {
        "data": {
            "labels": labels,
            "datasets": datasets
        },
        "type": "bar"
    }

def prepare_chart_data(job_card_details, filters):
    labels = []
    periodic_data = {
        "custom_total_input_qty": {},
        "total_completed_qty": {},
        "custom_scrap_qty": {}
    }

    filters.range = "Monthly"
    ranges = get_period_date_ranges(filters)

    for from_date, end_date in ranges:
        period = get_period(end_date, filters)
        if period not in labels:
            labels.append(period)

        for d in job_card_details:
            from_time = d.get("from_time")
            to_time = d.get("to_time")

            if from_time and to_time:
                if getdate(from_time) >= from_date and getdate(to_time) <= end_date:
                    for field in periodic_data:
                        val = flt(d.get(field))
                        if val > 0:
                            periodic_data[field][period] = periodic_data[field].get(period, 0) + val

    return labels, periodic_data

def calculate_totals(data):
    fields_to_sum = [
        "for_quantity",              
        "custom_total_input_qty",    
        "total_completed_qty",       
        "custom_scrap_qty",          
        "custom_total_setup_defect_qty", 
        "total_time_in_mins",        
    ]

    totals = {}
    for field in fields_to_sum:
        totals[field] = sum(flt(row.get(field, 0)) for row in data if flt(row.get(field, 0)) > 0)

    yield_value = round(totals["total_completed_qty"] / totals["custom_total_input_qty"], 2) if totals["custom_total_input_qty"] > 0 else 0

    denom = totals["custom_total_input_qty"] + totals["custom_total_setup_defect_qty"]
    yield_setup = round(totals["total_completed_qty"] / denom, 2) if denom > 0 else 0

    units_per_hour = round((totals["total_completed_qty"] / totals["total_time_in_mins"]) * 60, 2) if totals["total_time_in_mins"] > 0 else 0

    total_row = {
        "item_name": _("Total"),
        "for_quantity": totals["for_quantity"],
        "custom_total_input_qty": totals["custom_total_input_qty"],
        "total_completed_qty": totals["total_completed_qty"],
        "custom_scrap_qty": totals["custom_scrap_qty"],
        "custom_total_setup_defect_qty": totals["custom_total_setup_defect_qty"],
        "total_time_in_mins": totals["total_time_in_mins"],
        "custom_yield": yield_value,
        "custom_yield_setup": yield_setup,
        "custom_unit_hours": units_per_hour,
    }

    return total_row

def get_columns(filters):
    columns = [
        {"label": _("ID"), "fieldname": "name", "fieldtype": "Link", "options": "Job Card", "width": 100},
        {"label": _("Status"), "fieldname": "status", "width": 150},
        {"label": _("Job Card Name"), "fieldname": "custom_job_card_name", "fieldtype": "Link", "options": "Job Card", "width": 220},
        {"label": _("Work Order"), "fieldname": "work_order", "fieldtype": "Link", "options": "Work Order", "width": 180},
        {"label": _("Operation"), "fieldname": "operation", "fieldtype": "Link", "options": "Operation", "width": 100},
        {"label": _("Workstation"), "fieldname": "workstation", "fieldtype": "Link", "options": "Workstation", "width": 150},
        {"label": _("Workstation Type"), "fieldname": "workstation_type", "fieldtype": "Link", "options": "Workstation Type", "width": 150},
        {"label": _("Production Item"), "fieldname": "production_item", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 180},
        {"label": _("Qty on This Job Card"), "fieldname": "for_quantity", "fieldtype": "Float", "precision": 2, "width": 120},
        {"label": _("Total Input Qty"), "fieldname": "custom_total_input_qty", "fieldtype": "Float", "precision": 2, "width": 150},
        {"label": _("Total Completed Qty"), "fieldname": "total_completed_qty", "fieldtype": "Float", "precision": 2, "width": 150},
        {"label": _("Total Production Defect Qty"), "fieldname": "custom_scrap_qty", "fieldtype": "Float", "precision": 2, "width": 150},
        {"label": _("Yield"), "fieldname": "custom_yield", "fieldtype": "Percent",  "precision": 2, "width": 100},
        {"label": _("Total Setup Defect Qty"), "fieldname": "custom_total_setup_defect_qty", "fieldtype": "Float", "precision": 2, "width": 150},
        {"label": _("Yield (+Setup)"), "fieldname": "custom_yield_setup", "fieldtype": "Percent",  "precision": 2, "width": 150},
        {"label": _("Total Time In Mins"), "fieldname": "total_time_in_mins", "fieldtype": "Float", "precision": 2, "width": 150},
        {"label": _("Units / Hour"), "fieldname": "custom_unit_hours", "fieldtype": "Float", "precision": 2, "width": 150},
        {"label": _("Sequence"), "fieldname": "sequence", "fieldtype": "Int", "width": 80},
        {"label": _("Type"), "fieldname": "custom_type", "fieldtype": "Data", "width": 150},
        {"label": _("Shift"), "fieldname": "custom_shift", "fieldtype": "Data", "width": 80},
        {"label": _("Employee"), "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": _("From Time"), "fieldname": "from_time", "fieldtype": "Datetime", "width": 130},
        {"label": _("To Time"), "fieldname": "to_time", "fieldtype": "Datetime", "width": 130},
        {"label": _("Input Qty"), "fieldname": "custom_input_qty", "fieldtype": "Float", "precision": 2, "width": 100},
        {"label": _("Completed Qty"), "fieldname": "completed_qty", "fieldtype": "Float", "precision": 2, "width": 120},
        {"label": _("Defect Qty"), "fieldname": "qty", "fieldtype": "Float", "precision": 2, "width": 100},
        {"label": _("Defect Name"), "fieldname": "defect", "fieldtype": "Data", "width": 130},
        {"label": _("Time In Mins"), "fieldname": "time_in_mins", "fieldtype": "Float", "precision": 2, "width": 120},
        {"label": _("Units / Hour"), "fieldname": "custom_units_hour_log", "fieldtype": "Float", "precision": 2, "width": 150}
    ]
    return columns
