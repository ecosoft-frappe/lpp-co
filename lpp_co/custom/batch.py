# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.naming import make_autoname
from erpnext.stock.doctype.batch.batch import Batch

class BatchLPP(Batch):
	pass
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.series = f"XXXXX/.#####"

	# def autoname(self):
	# 	self.name = make_autoname(self.series) + "/YYYYY"
