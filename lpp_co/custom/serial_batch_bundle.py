# lpp_co/custom/serial_batch_bundle.py

import frappe
from frappe import bold
from frappe.utils import cint

def validate_qty_by_bypass(self, doc):
    allow_negative_stock = cint(frappe.db.get_single_value("Stock Settings", "allow_negative_stock"))

    if allow_negative_stock:
        return

    if doc.type_of_transaction == "Outward" and self.actual_qty and doc.total_qty:
        precision = doc.precision("total_qty")

        total_qty = frappe.utils.flt(abs(doc.total_qty), precision)
        required_qty = frappe.utils.flt(abs(self.actual_qty), precision)

        if required_qty - total_qty > 0:
            msg = f"For the item {bold(doc.item_code)}, the Available qty {bold(total_qty)} is less than the Required Qty {bold(required_qty)} in the warehouse {bold(doc.warehouse)}. Please add sufficient qty in the warehouse."
            frappe.throw(msg, title="Insufficient Stock")
