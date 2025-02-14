import frappe
from frappe import _


# Overwrite
def validate_stock_item_warehouse(row, item) -> None:
	if row.doctype in ["Purchase Receipt", "Purchase Receipt Item"] and item.is_stock_item == 1 and row.qty and not row.warehouse and not row.get("delivered_by_supplier"):
		frappe.throw(
			_("Row #{1}: Warehouse is mandatory for stock Item {0}").format(
				frappe.bold(row.item_code), row.idx
			)
		)
