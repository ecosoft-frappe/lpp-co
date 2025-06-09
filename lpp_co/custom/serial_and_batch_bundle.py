import frappe
from frappe import _
from frappe import bold
from frappe.utils import cint
from erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle import SerialandBatchBundle

# class SerialandBatchBundleLPP(SerialandBatchBundle):
    
# 	def set_serial_and_batch_values(self, parent, row, qty_field=None):
# 		# Auto adjust batch bundle qty to avoid warning, for a very specific case
# 		if (
#       		parent.doctype == "Stock Entry"
#         	and parent.stock_entry_type == "Manufacture"
#          	and self.has_batch_no
# 			and self.type_of_transaction == "Inward"
# 		):
# 			# Case using batch (not serial), assume only 1 batch
# 			self.entries[0].qty = row.transfer_qty
# 			self.save()
# 		super().set_serial_and_batch_values(parent, row, qty_field=qty_field)

class SerialandBatchBundleLPP(SerialandBatchBundle):

    def validate_negative_batch(self, batch_no, available_qty):
        allow_negative_stock = cint(frappe.db.get_single_value("Stock Settings", "allow_negative_stock"))

        if allow_negative_stock:
            return

        if available_qty < 0 and not self.is_stock_reco_for_valuation_adjustment(available_qty):
            msg = f"""Batch No {bold(batch_no)} of an Item {bold(self.item_code)}
                has negative stock
                of quantity {bold(available_qty)} in the
                warehouse {self.warehouse}"""

            frappe.throw(_(msg), BatchNegativeStockError)