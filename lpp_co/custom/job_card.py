import frappe
from frappe import _
from erpnext.manufacturing.doctype.job_card.job_card import JobCard


class JobCardLPP(JobCard):

	@property
	def time_log(self):
		sequence = int(self.custom_sequence or 0)
		if self.time_logs:
			time_log_by_sequence = list(filter(
				lambda k: k.idx == sequence, self.time_logs))
			if time_log_by_sequence:
				return time_log_by_sequence[0]
		return None

	@property
	def operator(self):
		if self.time_log:
			employee = self.time_log.employee
			if employee:
				return frappe.get_value("Employee", employee, "employee_name")
		return ""

	@property
	def shift(self):
		return self.time_log and self.time_log.custom_shift or ""

	@property
	def from_time(self):
		return self.time_log and self.time_log.from_time or ""

	@property
	def to_time(self):
		return self.time_log and self.time_log.to_time or ""

	@property
	def input(self):
		return self.time_log and self.time_log.custom_input_qty or 0

	@property
	def output(self):
		return self.time_log and self.time_log.completed_qty or 0

	@property
	def defect(self):
		return self.input - self.output

	@property
	def percent_yield(self):
		if self.input > 0:
			return round(self.output / self.input * 100, 2)
		else:
			return 0

	@property
	def job_card_defect(self):
		return self.get("custom_job_card_defect_%s" % self.custom_sequence)

	@property
	def next_operation(self):
		if self.custom_run_step:
			next_step = self.custom_run_step + 1
			# Get the next job card
			next_operation = frappe.get_value(
				"Job Card",
				{
					"work_order": self.work_order,
					"custom_run_card": self.custom_run_card,
					"custom_run_step": next_step,
					"docstatus": ("!=", 2),
				},
				"operation"
			)
			return next_operation or "-"
		return "-- END --"

	def get_overlap_for(self, args, open_job_cards=None):
		# Overwrite: LPP need to overlap time log for employee can work multi job card in same time
		return {}

	def validate_sequence_id(self):
		if self.docstatus == 0:
			return
		return super().validate_sequence_id()

def time_log(self):
		sequence = int(self.custom_sequence or 0)
		if self.time_logs:
			time_log_by_sequence = list(filter(
				lambda k: k.idx == sequence and k.custom_type == "Production", self.time_logs))
			if time_log_by_sequence:
				return time_log_by_sequence[0]
		return None

def set_sequence_input_quantity(doc, method):
	# on child table time log, set the quantity to sum of quantity in table job_card_defects
	sequences = len(doc.time_logs)
	if sequences > 6:
		frappe.throw(_("Time Logs > 6 lines is not supported"))
	
	total_defects = 0
	total_setup_defects = 0

	for seq in range(sequences):
		if seq+1 > 6:
			continue
		
		time_log = doc.time_logs[seq]
		
		if time_log.custom_type == "Production":
			defects = sum([defect.qty for defect in doc.get("custom_job_card_defect_%s" % str(seq+1))])
			total_defects += defects
			time_log.custom_input_qty = time_log.completed_qty + defects
		
		elif time_log.custom_type == "Setup":
			setup_defects = sum([defect.qty for defect in doc.get("custom_job_card_defect_%s" % str(seq+1))])
			total_setup_defects += setup_defects

	doc.custom_scrap_qty = total_defects
	doc.custom_total_setup_defect_qty = total_setup_defects

	doc.custom_total_input_qty = (doc.total_completed_qty) + (doc.custom_scrap_qty)
	doc.custom_yield = (doc.total_completed_qty) / (doc.custom_total_input_qty) * 100
	doc.custom_yield_setup = ( doc.total_completed_qty / (doc.custom_total_input_qty + doc.custom_total_setup_defect_qty) ) * 100


def validate_time_log_and_defect(doc, method):
	sequences = len(doc.time_logs)
	for seq in range(6):
		defects = sum([defect.qty for defect in doc.get("custom_job_card_defect_%s" % str(seq+1))])
		if defects > 0 and sequences < seq+1:
			frappe.throw(_("Job Card Defect {} cannot be entered without Time Log No. {}").format(seq+1, seq+1))


def update_scrap_qty_to_work_order(doc, method):
	"""Update scrap qty to work order"""
	if doc.custom_scrap_qty > 0:
		job_cards = frappe.get_all(
			"Job Card",
			filters={"work_order": doc.work_order, "docstatus": 1},
			fields=["name", "custom_scrap_qty"]
		)
		total_scrap_qty = sum([job_card.custom_scrap_qty for job_card in job_cards])
		frappe.db.set_value("Work Order", doc.work_order, "custom_scrap_qty", total_scrap_qty, update_modified=False)


@frappe.whitelist()
def get_bom_items(bom):
	items = frappe.db.get_all("BOM Item", filters={"parent": bom}, pluck="item_code")
	return items
