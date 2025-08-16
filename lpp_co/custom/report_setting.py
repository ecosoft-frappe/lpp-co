import frappe


def delete_report():
    reports = [
        "Stock Ledger",
    ]
    for report in reports:
        frappe.db.sql("""
            delete from `tabReport` where name = %s
        """, report)
