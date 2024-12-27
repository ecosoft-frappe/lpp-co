# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import PurchaseReceipt
from frappe import _


class LPPPurchaseReceipt(PurchaseReceipt):
	def validate_qi_presence_after_submit(self, row):
		"""Check if QI is present on row level. Warn on submit if missing."""
		if not row.quality_inspection:
			msg = _("Row #{0}: Quality Inspection is required for Item {1}").format(
				row.idx, frappe.bold(row.item_code)
			)
			frappe.msgprint(msg, title=_("Inspection Required"), indicator="blue")

	def validate_inspection_after_submit(self):
		for row in self.get("items"):
			qi_required = False
			if frappe.db.get_value(
				"Item", row.item_code, "custom_inspection_required_after_purchase_receipt"
			):
				qi_required = True

			if row.get("is_scrap_item"):
				continue

			if qi_required:  # validate row only if inspection is required on item level
				self.validate_qi_presence_after_submit(row)

	def on_submit(self):
		super().on_submit()
		# Validate inspection required after purchase receipt
		if not self.get("is_return"):
			self.validate_inspection_after_submit()
