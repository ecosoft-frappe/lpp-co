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
	operations = frappe.get_all("Job Card", filters={"work_order": doc.name}, distinct=True, pluck="operation")
	for operation in operations:
		job_cards = frappe.get_all(
      		"Job Card",
        	filters={
             	"work_order": doc.name,
              	"operation": operation,
				"docstatus": 0
            },
         	order_by="creation asc"
        )
		total_run_card_set = str(len(job_cards)).zfill(3)
		for idx, job_card in enumerate(job_cards, start=1):
			run_card_set = str(idx).zfill(3)
			run_card = f"{run_card_set}/{total_run_card_set}"
			frappe.db.set_value("Job Card", job_card.name, "custom_run_card", run_card)
   

def set_run_card_step(doc):
	run_cards = frappe.get_all("Job Card", filters={"work_order": doc.name}, distinct=True, pluck="custom_run_card")
	for run_card in run_cards:
		job_cards = frappe.get_all(
      		"Job Card",
        	filters={
             	"work_order": doc.name,
              	"custom_run_card": run_card,
				"docstatus": 0
            },
         	order_by="creation asc"
        )
		for idx, job_card in enumerate(job_cards, start=1):
			frappe.db.set_value("Job Card", job_card.name, "custom_run_step", idx)


def set_job_card_name(doc):
	job_cards = frappe.get_all(
    	"Job Card",
     	filters={"work_order": doc.name},
      	fields=["name", "custom_run_card", "custom_run_step"],
       	as_list=1
    )
	for (job_card, run_card, run_step) in job_cards:
		frappe.db.set_value("Job Card", job_card, "custom_job_card_name", f"{doc.name}-{run_card}-{run_step}")
