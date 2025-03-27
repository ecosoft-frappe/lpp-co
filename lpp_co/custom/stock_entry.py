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
