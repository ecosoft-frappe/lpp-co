import frappe
from frappe import _
from frappe.utils import flt
from erpnext.stock.doctype.serial_no.serial_no import get_serial_nos
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

	def validate_batch(self):
		if self.purpose == "Repack":
			for item in self.get("items"):
				if item.batch_no and frappe.db.get_value("Batch", item.batch_no, "disabled") == 1:
					frappe.throw(
						_("Batch {0} of Item {1} is disabled.").format(item.batch_no, item.item_code)
					)
		else:
			super().validate_batch()

	def validate_serialized_batch(self):
		if self.purpose == "Repack":
			for d in self.get("items"):
				if hasattr(d, "serial_no") and hasattr(d, "batch_no") and d.serial_no and d.batch_no:
					serial_nos = frappe.get_all(
						"Serial No",
						fields=["batch_no", "name", "warehouse"],
						filters={"name": ("in", get_serial_nos(d.serial_no))},
					)
					for row in serial_nos:
						if row.warehouse and row.batch_no != d.batch_no:
							frappe.throw(
								_("Row #{0}: Serial No {1} does not belong to Batch {2}").format(
									d.idx, row.name, d.batch_no
								)
							)
		else:
			super().validate_serialized_batch()
