import frappe


def get_sales_order_qty(doc, method):
    doc.custom_sales_order_qty = frappe.db.get_value("Sales Order Item", doc.sales_order_item, "qty")
