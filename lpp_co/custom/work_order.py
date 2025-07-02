import frappe
from erpnext.manufacturing.doctype.work_order.work_order import WorkOrder


class WorkOrderLPP(WorkOrder):
    
	# @property
	# def customer(self):
	# 	sales_order = frappe.get_cached_doc("Sales Order", self.sales_order)
	# 	return sales_order.customer

	@property
	def customer_item(self):
		item = frappe.get_doc("Item", self.production_item)
		customer_item = list(filter(lambda l: l.customer_name == self.custom_customer, item.customer_items))
		if customer_item:
			return customer_item[0]
		return None

	@property
	def material(self):
		if self.customer_item:
			return self.customer_item.custom_material or ""
		return ""

	@property
	def drawing_build_sheet_no(self):
		if self.customer_item:
			return self.customer_item.custom_drawing_build_sheet_no or ""
		return ""


def get_sales_order_qty(doc, method):
    doc.custom_sales_order_qty = frappe.db.get_value("Sales Order Item", doc.sales_order_item, "qty")


def set_run_card(doc, method):
	# Set Run Card, i.e. 1/6, 2/6
	set_run_card_set(doc)	
	# Set Run Step in each Run Card Number, i..e, in 1/6, there should be step 1, 2, 3
	set_run_card_step(doc)
	# Set Job Card Name, i.e., WO2502-0001-010/090-1, WO2502-0001-010/090-2
	set_job_card_name(doc)
 
 
def set_run_card_set(doc):
	job_cards = frappe.get_all(
		"Job Card",
		filters={"work_order": doc.name, "docstatus": 0},
		fields=["name", "operation"],
		order_by="creation"
	)

	op_groups = {}
	for jc in job_cards:
		op_groups.setdefault(jc["operation"], []).append(jc["name"])

	max_batch = max(len(jcs) for jcs in op_groups.values())

	for i in range(max_batch):
		run_card = f"{i+1:03}/{max_batch:03}"
		for jcs in op_groups.values():
			if i < len(jcs):
				frappe.db.set_value("Job Card", jcs[i], "custom_run_card", run_card)


def set_run_card_step(doc):
	op_order = {
		op.operation: idx + 1
		for idx, op in enumerate(sorted(doc.operations, key=lambda x: x.idx))
	}

	job_cards = frappe.get_all(
		"Job Card",
		filters={"work_order": doc.name, "docstatus": 0},
		fields=["name", "custom_run_card", "operation"]
	)

	run_groups = {}
	for jc in job_cards:
		run_groups.setdefault(jc["custom_run_card"], []).append(jc)

	for group in run_groups.values():
		for jc in group:
			if jc["operation"] in op_order:
				frappe.db.set_value("Job Card", jc["name"], "custom_run_step", op_order[jc["operation"]])


def set_job_card_name(doc):
	job_cards = frappe.get_all(
    	"Job Card",
     	filters={"work_order": doc.name},
      	fields=["name", "custom_run_card", "custom_run_step"],
       	as_list=1
    )
	for (job_card, run_card, run_step) in job_cards:
		frappe.db.set_value("Job Card", job_card, "custom_job_card_name", f"{doc.name}-{run_card}-{run_step}")
