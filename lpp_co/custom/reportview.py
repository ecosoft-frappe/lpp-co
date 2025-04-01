import re
import json
import frappe
from frappe import _
from frappe.desk.reportview import get_form_params
from frappe.desk.reportview import append_totals_row
from frappe.desk.reportview import get_field_info
from frappe.desk.reportview import handle_duration_fieldtype_values
from frappe.core.doctype.access_log.access_log import make_access_log
from frappe.model.db_query import DatabaseQuery


# Overwrite
@frappe.whitelist()
@frappe.read_only()
def export_query():
	"""export from report builder"""
	from frappe.desk.utils import get_csv_bytes, pop_csv_params, provide_binary_file

	form_params = get_form_params()

	if "fields" in form_params:
		# Remove docstatus
		form_params["fields"] = list(
			filter(lambda field: not re.search(r"(?i)(\.|`)docstatus(?=\W|$)", field), form_params.get("fields", [])))

		# Remove some field not need (not recomended)
		form_params["fields"] = list(
			filter(lambda field: not re.search(r"as\s*'Material Request Item:name'", field), form_params.get("fields", [])))

	form_params["limit_page_length"] = None
	form_params["as_list"] = True
	doctype = form_params.pop("doctype")

	# Remove owner
	# if isinstance(form_params["fields"], list):
	# 	form_params["fields"].append("owner")
	# elif isinstance(form_params["fields"], tuple):
	# 	form_params["fields"] = form_params["fields"] + ("owner",)

	file_format_type = form_params.pop("file_format_type")
	title = form_params.pop("title", doctype)
	csv_params = pop_csv_params(form_params)
	add_totals_row = 1 if form_params.pop("add_totals_row", None) == "1" else None
	translate_values = 1 if form_params.pop("translate_values", None) == "1" else None

	if selection := form_params.pop("selected_items", None):
		form_params["filters"] = {"name": ("in", json.loads(selection))}

	make_access_log(
		doctype=doctype,
		file_type=file_format_type,
		report_name=form_params.report_name,
		filters=form_params.filters,
	)

	db_query = DatabaseQuery(doctype)
	ret = db_query.execute(**form_params)

	if not frappe.permissions.can_export(doctype):
		if frappe.permissions.can_export(doctype, is_owner=True):
			for row in ret:
				if row[-1] != frappe.session.user:
					raise frappe.PermissionError(
						_("You are not allowed to export {} doctype").format(doctype)
					)
		else:
			raise frappe.PermissionError(_("You are not allowed to export {} doctype").format(doctype))

	if add_totals_row:
		ret = append_totals_row(ret)

	fields_info = get_field_info(db_query.fields, doctype)

	labels = [info["label"] for info in fields_info]
	data = [[_("Sr"), *labels]]
	processed_data = []

	if frappe.local.lang == "en" or not translate_values:
		data.extend([i + 1, *list(row)] for i, row in enumerate(ret))
	elif translate_values:
		translatable_fields = [field["translatable"] for field in fields_info]
		processed_data = []
		for i, row in enumerate(ret):
			processed_row = [i + 1] + [
				_(value) if translatable_fields[idx] else value for idx, value in enumerate(row)
			]
			processed_data.append(processed_row)
		data.extend(processed_data)

	data = handle_duration_fieldtype_values(doctype, data, db_query.fields)

	if file_format_type == "CSV":
		from frappe.utils.xlsxutils import handle_html

		file_extension = "csv"
		content = get_csv_bytes(
			[[handle_html(frappe.as_unicode(v)) if isinstance(v, str) else v for v in r] for r in data],
			csv_params,
		)
	elif file_format_type == "Excel":
		from frappe.utils.xlsxutils import make_xlsx

		file_extension = "xlsx"
		content = make_xlsx(data, doctype).getvalue()

	provide_binary_file(title, file_extension, content)
