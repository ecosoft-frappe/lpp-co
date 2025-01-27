app_name = "lpp_co"
app_title = "LPP Co"
app_publisher = "Ecosoft"
app_description = "LPP Co's ERP"
app_email = "tharathipc@ecosoft.co.th"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "lpp_co",
# 		"logo": "/assets/lpp_co/logo.png",
# 		"title": "LPP Co",
# 		"route": "/lpp_co",
# 		"has_permission": "lpp_co.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/lpp_co/css/lpp_co.css"
# app_include_js = "/assets/lpp_co/js/lpp_co.js"

# include js, css files in header of web template
# web_include_css = "/assets/lpp_co/css/lpp_co.css"
# web_include_js = "/assets/lpp_co/js/lpp_co.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "lpp_co/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views

doctype_js = {
	"Purchase Receipt": "public/js/purchase_receipt.js",
	"Quality Inspection": "public/js/quality_inspection.js",
	"Quotation": "public/js/quotation.js",
	"Sales Order": "public/js/sales_order.js",
	"Item": "public/js/item.js",
	"Material Request": "public/js/material_request.js"
}

doctype_list_js = {
	"Item": "public/js/item_list.js",
	"Item Group": "public/js/item_group_list.js",
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "lpp_co/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
	"methods": [
		"qr_demo.qr_code.get_qr_code",
		"lpp_co.utils.jinja_methods",
	],
	"filters": "lpp_co.utils.jinja_filters",
}

# Installation
# ------------

# before_install = "lpp_co.install.before_install"
# after_install = "lpp_co.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "lpp_co.uninstall.before_uninstall"
# after_uninstall = "lpp_co.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "lpp_co.utils.before_app_install"
# after_app_install = "lpp_co.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "lpp_co.utils.before_app_uninstall"
# after_app_uninstall = "lpp_co.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lpp_co.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Item": "lpp_co.custom.item.ItemLPP",
	"Quality Inspection": "lpp_co.custom.quality_inspection.QualityInspectionLPP",
	"Material Request": "lpp_co.custom.material_request.MaterialRequestLPP",
	"Batch": "lpp_co.custom.batch.BatchLPP",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Item": {
		"on_update": "lpp_co.custom.item_group_tag.update_item_group_tags",
	},
	"Item Group": {
		"on_update": [
			"lpp_co.custom.item_group_tag.prepare_group_tags",
		]
	},
	"Sales Order": {
		"on_update": ["lpp_co.custom.quotation.validate_customer_item"]
	},
	"Quotation": {
		"on_update": ["lpp_co.custom.quotation.validate_customer_item"]
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"lpp_co.tasks.all"
# 	],
# 	"daily": [
# 		"lpp_co.tasks.daily"
# 	],
# 	"hourly": [
# 		"lpp_co.tasks.hourly"
# 	],
# 	"weekly": [
# 		"lpp_co.tasks.weekly"
# 	],
# 	"monthly": [
# 		"lpp_co.tasks.monthly"
# 	],
# }
scheduler_events = {
	"daily": ["lpp_co.custom.item_group_tag.prepare_group_tags"],
}
# Testing
# -------

# before_tests = "lpp_co.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "lpp_co.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "lpp_co.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["lpp_co.utils.before_request"]
# after_request = ["lpp_co.utils.after_request"]

# Job Events
# ----------
# before_job = ["lpp_co.utils.before_job"]
# after_job = ["lpp_co.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"lpp_co.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
	{
		"dt": "Custom Field",
		"filters": [
			[
				"name",
				"in",
				[
					"Item-custom_item_specification_line",
					"Item-custom_section_break_uyyv3",
					"Item-custom_item_tag_3",
					"Item-custom_item_tag_2",
					"Item-custom_item_tag_1",
					"Item-custom_search_tags",
					"Item-custom_item_group_1_abbr",
					"Item-custom_specifications__tolerance",
					"Item-custom_reset_quality_parameters",
					"Item-custom_item_group_1_name",
					"Item-custom_item_group_1",
					"Item-custom_item_group_2_name",
					"Item-custom_item_group_2",
					"Item-custom_item_group_name",
					"Item-custom_unit_box",
					"Item-custom_column_break_yjasg",
					"Item-custom_unit_pack",
					"Item-custom_print_label",
					"Address-custom_branch",
					"Payment Entry Reference-custom_remark",
					# "Quality Inspection Parameter-custom_is_item_spec",
					# "Item Group-custom_quality_inspection_parameter_group",
					"Item Group-custom_abbreviation",
					"Quality Inspection-custom_open_quality_inspection_result",
					"Quality Inspection-custom_open_functional_testing",
					"Quality Inspection-custom_open_specification_inspection",
					"Quality Inspection-custom_open_visual_inspection",
					"Quality Inspection-custom_column_break_4qn0t",
					# "Quality Inspection-custom_quality_inspection_type",
					"Quality Inspection-custom_column_break_f29q1",
					# "Quality Inspection-custom_quality_inspection_process",
					"Quality Inspection-custom_section_break_ud4co",
					"Quality Inspection-custom_inspection_results",
					"Quality Inspection-custom_visual_inspection",
					"Quality Inspection-custom_visual_inspection_html",
					"Quality Inspection-custom_specification_inspection",
					"Quality Inspection-custom_specification_inspection_html",
					"Quality Inspection-custom_functional_testing",
					"Quality Inspection-custom_functional_testing_html",
					# "Quality Inspection-custom_column_break_mhnva",
					# "Quality Inspection-custom_section_break_236ps",
					"Quality Inspection Template-custom_for_doctype",
					"Item Customer Detail-custom_lpp_part_no",
					"Item Customer Detail-custom_material",
					"Item Customer Detail-custom_drawing_build_sheet_no",
					"Item Quality Inspection Parameter-custom_inspection_method",
					"Quality Inspection Parameter-custom_related_item_groups",
					"Material Request-custom_sample_record",
					"Material Request-custom_status_of_sample_record",
					"Material Request-custom_column_break_yi4jl",
     				"Material Request-custom_priority",
     				"Material Request-custom_sample_record_info",
					"Material Request-custom_column_break_h6k5j",
					"Material Request-custom_qa_acknowledgement",
					"Material Request-custom_mkt_acknowledgement",
					"Material Request-custom_operated_by",
					"Material Request-custom_section_break_ho5bc",
					"Material Request-custom_plan_customer_delivery",
					"Material Request-custom_plan_sample_production",
					"Material Request-custom_plan_mold_creation",
					"Material Request-custom_status_customer_delivery",
					"Material Request-custom_status_sample_production",
					"Material Request-custom_actual_remark",
					"Material Request-custom_actual_customer_delivery",
					"Material Request-custom_actual_sample_production",
					"Material Request-custom_actual_mold_creation",
					"Material Request-custom_plan_remark",
					"Material Request-custom_planned",
					"Material Request-custom_status_mold_creation",
					"Material Request-custom_column_break_yivb6",
					"Material Request-custom_column_break_p4icq",
					"Material Request-custom_section_break_dskvi",
					"Material Request-custom_first_production_work_order",
					"Material Request-custom_first_production_lesson_learnt",
					"Material Request-custom_column_break_bwn2b",
					"Material Request-custom_first_production_action",
					"Material Request-custom_column_break_yeonm",
					"Material Request-custom_first_production_problem",
					"Material Request-custom_section_break_giwrt",
					"Material Request-custom_sample_production_lesson_learnt",
					"Material Request-custom_column_break_ntdfo",
					"Material Request-custom_sample_production_action",
					"Material Request-custom_column_break_wukc0",
					"Material Request-custom_sample_production_problem",
					"Material Request-custom_section_break_zh4rg",
					"Material Request-custom_column_break_0dldz",
					"Material Request-custom_mold_item",
					"Material Request-custom_section_break_1vgrd",
					"Purchase Receipt-custom_supplier_invoice_date",
					"Purchase Receipt-custom_column_break_5dhmu",
					"Purchase Receipt-custom_supplier_invoice_number",
					"Purchase Receipt-custom_supplier_invoice",
					"GL Entry-custom_cost_center_2",
					"GL Entry-custom_cost_center_1",
				],
			]
		],
	},
	{
		"dt": "Property Setter",
		"filters": [
			[
				"name",
				"in",
				[
					"Item-main-field_order",
					"Item-item_group-label",
					"Item-inspection_required_before_delivery-hidden",
					"Item-inspection_required_before_purchase-hidden",
					"Item-naming_series-default",
					"Item-naming_series-options",
					"Quality Inspection Reading-acceptance_formula-description",
					"Item Group-item_group_name-unique",
					"Item Group-main-title_field",
					"Item Group-main-autoname",
					"Item Group-main-naming_rule",
					"Item Customer Detail-ref_code-label",
					"Quality Inspection-reference_type-options",
     				"Quality Inspection-status-label",
					"Quality Inspection-manual_inspection-default",
					"Quality Inspection-manual_inspection-read_only",
					"Quality Inspection-item_serial_no-hidden",
					"Quality Inspection-readings-hidden",
					"Quality Inspection-main-field_order",
					"Quality Inspection-reference_type-options",
					"Quality Inspection-inspection_type-read_only",
					"Item Quality Inspection Parameter-acceptance_formula-description",
					"Item Quality Inspection Parameter-acceptance_formula-hidden",
					"Item Quality Inspection Parameter-formula_based_criteria-hidden",
					"Item Quality Inspection Parameter-max_value-hidden",
					"Item Quality Inspection Parameter-min_value-hidden",
					"Item Quality Inspection Parameter-numeric-hidden",
					"Item Quality Inspection Parameter-value-hidden",
					"Item Quality Inspection Parameter-parameter_group-hidden",
					"Item Quality Inspection Parameter-main-field_order",
					"Item Customer Detail-main-field_order",
					"Material Request-main-field_order",
					"Material Request-customer-depends_on",
					"GL Entry-cost_center-label",
				],
			]
		],
	},
	{
		"dt": "Client Script",
		"filters": [
			[
				"name",
				"in",
				[
					"Print PDF - Job Card",
					"Print PDF - Purchase Receipt",
					"Print PDF - Delivery Note",
					"Print PDF - Sales Order",
					"Print PDF - Purchase Order",
					"Print PDF - Sales Billing",
					"Print PDF - Quotation",
					"Print PDF - Purchase Invoice",
					"Print PDF - Payment Entry",
					"Print PDF - Work Order",
					"Print PDF - Journal Entry",
					"Print PDF - Sales Invoice",
				],
			]
		]
	},
]


cost_center_field_doctypes = [
	"Advance Taxes and Charges",
	"Asset",
	"Asset Capitalization",
	"Asset Capitalization Asset Item",
	"Asset Capitalization Service Item",
	"Asset Capitalization Stock Item",
	"Delivery Note",
	"Delivery Note Item",
	"Expense Claim",
	"Expense Claim Detail",
	"Expense Taxes and Charges",
	"Journal Entry Account",
	"Landed Cost Item",
	"Material Request Item",
	"Payment Entry",
	"Purchase Invoice",
	"Purchase Invoice Item",
	"Purchase Order",
	"Purchase Order Item",
	"Purchase Receipt",
	"Purchase Receipt Item",
	"Purchase Taxes and Charges",
	"Sales Invoice",
	"Sales Order",
	"Sales Taxes and Charges",
	# "Stock Entry Detail",
	"Subcontracting Order",
	"Subcontracting Order Item",
	"Subcontracting Receipt",
	"Subcontracting Receipt Item",
	"Supplier Quotation",
	"Supplier Quotation Item",
]
