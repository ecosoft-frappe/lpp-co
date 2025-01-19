# Copyright (c) 2025, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class QualityInspectionResult(Document):
	
	def validate(self):
		self.validate_updatable()
		self.set_accepted_rejected()
		self.set_sepcification()

	def on_trash(self):
		self.validate_updatable()

	def validate_updatable(self):
		qi = frappe.get_doc("Quality Inspection", self.quality_inspection)
		if qi.docstatus != 0:
			status = qi.docstatus == 1 and _("submitted") or _("cancelled")
			frappe.throw(
       			_("Modificatin of this result is not allowed!"
            	  "<br/>Quality Inspection {} is already {}.")
          		.format(self.quality_inspection, status)
        	)

	def set_accepted_rejected(self):
		self.qty_accepted = len(list(filter(lambda r: r.result == "Accepted", self.readings)))
		self.qty_rejected = len(list(filter(lambda r: r.result == "Rejected", self.readings)))

	def set_sepcification(self):
		item = frappe.get_cached_doc("Item", self.item)
		def get_item_specification():
			for spec in item.custom_item_specification_line:
				if spec.specification == self.parameter:
					return spec
			return None
		spec = get_item_specification()
		if spec:
			self.nominal = spec.nominal
			self.delta_plus = spec.delta_plus
			self.delta_minus = spec.delta_minus