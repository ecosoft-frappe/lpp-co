import frappe
from frappe import _
from erpnext.stock.doctype.material_request.material_request import MaterialRequest


class MaterialRequestLPP(MaterialRequest):

	def validate_material_request_type(self):
		""" Override """
		if self.material_request_type not in ("Manufacture", "Customer Provided"):
			self.customer = None
   
		if self.material_request_type == "Manufacture" and not self.custom_sample_record:
			self.customer = None

		if self.material_request_type != "Manufacture":
			self.custom_sample_record = 0

@frappe.whitelist()
def set_status(plan, actual):
	if plan and actual:
		return "On Time" if plan >= actual else "Late"
	return "-"

def set_sample_record_punctual_status(doc, method):
	""" Validate if the sample record is punctual """

	frappe.db.set_value(
     	"Material Request", doc.name,
      	"custom_status_mold_creation", set_status(doc.custom_plan_mold_creation, doc.custom_actual_mold_creation)
    )
	frappe.db.set_value(
     	"Material Request", doc.name,
      	"custom_status_sample_production", set_status(doc.custom_plan_sample_production, doc.custom_actual_sample_production)
    )
	frappe.db.set_value(
     	"Material Request", doc.name,
      	"custom_status_customer_delivery", set_status(doc.custom_plan_customer_delivery, doc.custom_actual_customer_delivery)
    )
	doc.reload()