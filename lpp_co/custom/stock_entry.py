import frappe
from frappe.utils import flt
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry


class StockEntryLPP(StockEntry):

	def validate_fg_completed_qty(self):
		if self.custom_allow_overwrite_fg_qty and self.purpose == "Manufacture" and self.work_order:
			for d in self.items:
				if d.is_finished_item:
					if self.process_loss_qty:
						self.process_loss_qty = self.fg_completed_qty - d.qty
						self.process_loss_percentage = flt(self.process_loss_qty * 100 / self.fg_completed_qty)

		super().validate_fg_completed_qty()
  
	def before_insert(self):
		# In LPP we don't want to use serial and batch bundle, we want user to choose Batch
		if self.custom_allow_overwrite_fg_qty and self.purpose == "Manufacture" and self.work_order:
			for item in self.items:
				if item.is_finished_item:
					# Use batch from batch bundle
					bundle = frappe.get_doc("Serial and Batch Bundle", item.serial_and_batch_bundle)
					if bundle:
						if bundle.entries[:1]:
							item.batch_no = bundle.entries[0].batch_no
						item.serial_and_batch_bundle = None