from erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle import SerialandBatchBundle


class SerialandBatchBundleLPP(SerialandBatchBundle):
    
	def set_serial_and_batch_values(self, parent, row, qty_field=None):
		# Auto adjust batch bundle qty to avoid warning, for a very specific case
		if (
      		parent.doctype == "Stock Entry"
        	and parent.stock_entry_type == "Manufacture"
         	and self.has_batch_no
			and self.type_of_transaction == "Inward"
		):
			# Case using batch (not serial), assume only 1 batch
			self.entries[0].qty = row.transfer_qty
			self.save()
		super().set_serial_and_batch_values(parent, row, qty_field=qty_field)
