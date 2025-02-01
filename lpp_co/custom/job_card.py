import frappe
from erpnext.manufacturing.doctype.job_card.job_card import JobCard


class JobCardLPP(JobCard):

	@property
	def time_log(self):
		sequence = int(self.custom_sequence or 0)
		if len(self.time_logs) == sequence:
			return self.time_logs[sequence-1]
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
	def next_station(self):
		if self.custom_run_step:
			next_step = self.custom_run_step + 1
			# Get the next job card
			next_workstation = frappe.get_value(
				"Job Card",
				{
					"work_order": self.work_order,
					"custom_run_card": self.custom_run_card,
					"custom_run_step": next_step,
				},
				"workstation"
			)
			return next_workstation or "-"
		return "-- END --"


def set_sequence_input_quantity(doc, method):
	# on child table time log, set the quantity to sum of quantity in table job_card_defects
	sequences = len(doc.time_logs)
	for seq in range(sequences):
		if seq+1 > 3:
			continue
		defects = sum([defect.qty for defect in doc.get("custom_job_card_defect_%s" % str(seq+1))])
		doc.time_logs[seq].custom_input_qty = doc.time_logs[seq].completed_qty + defects