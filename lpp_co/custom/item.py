# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from erpnext.stock.doctype.item.item import Item
from frappe.utils.nestedset import get_ancestors_of
from frappe import _


class ItemLPP(Item):

	def validate_item_specification_line(self):
		# Validate unique parameter in the item
		specifications = [line.specification for line in self.custom_item_specification_line]
		if len(specifications) != len(set(specifications)):
			frappe.throw(_("Parameter must be unique"))

	def validate(self):
		self.validate_item_specification_line()
		self.set_field_customer_items()
		super().validate()

	def set_field_customer_items(self):
		# This will be used as search field
		row_search = []
		ref_codes = []
		sheet_nos = []
		for row in self.customer_items:
			row_search.append(
       			" ".join([str(row.get(f) or "")
                for f in [
                	"customer_name",
                 	"custom_drawing_build_sheet_no",
                  	"ref_code",
                   	"custom_lpp_part_no"
                ]]))
			ref_codes.append(row.ref_code)
			sheet_nos.append(row.custom_drawing_build_sheet_no)
		self.custom_search_customer_items = ", ".join(row_search) or ""
		self.custom_ref_code = ", ".join(ref_codes) or ""
		self.custom_drawing_build_sheet_no = ", ".join(sheet_nos) or ""

	@frappe.whitelist()
	def get_item_quality_specification(self):
		# Find item specification groups related to this item
		item_groups = get_ancestors_of("Item Group", self.item_group)
		item_groups.append(self.item_group)
		params = frappe.get_all(
      		"Quality Inspection Parameter",
        	filters=[
				["Quality Inspection Parameter Item Group",
     			 "item_group", "in", item_groups]
			],
         	pluck="name",
        	order_by="name"
        )
		return list(set(params))

