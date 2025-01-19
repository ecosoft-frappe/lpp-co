import frappe # type: ignore
from erpnext.stock.doctype.material_request.material_request import MaterialRequest


class MaterialRequestLPP(MaterialRequest):

	def validate(self):
		self.validate_sample_record_punctual_status()
		super().validate()
  
	def validate_sample_record_punctual_status(self):
		def set_status(plan, actual):
			if plan and actual:
				return "On Time" if plan >= actual else "Late"
			return "-"
			
		self.custom_status_mold_creation = set_status(self.custom_plan_mold_creation, self.custom_actual_mold_creation)
		self.custom_status_sample_production = set_status(self.custom_plan_sample_production, self.custom_actual_sample_production)
		self.custom_status_customer_delivery = set_status(self.custom_plan_customer_delivery, self.custom_actual_customer_delivery)

	def validate_material_request_type(self):
		""" Override """
		if self.material_request_type not in ("Manufacture", "Customer Provided"):
			self.customer = None
   
		if self.material_request_type != "Manufacture":
			self.custom_sample_record = 0
