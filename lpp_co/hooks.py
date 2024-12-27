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
}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
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
# jinja = {
# 	"methods": "lpp_co.utils.jinja_methods",
# 	"filters": "lpp_co.utils.jinja_filters"
# }

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
	"Item": "lpp_co.custom.item.LPPItem",
	"Purchase Receipt": "lpp_co.custom.purchase_receipt.LPPPurchaseReceipt",
	"Quality Inspection": "lpp_co.custom.quality_inspection.LPPQualityInspection",
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

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
					"Item-custom_inspection_required_after_purchase_receipt",
					"Item-custom_item_specification_line",
					"Item-custom_section_break_uyyv3",
					"Item-custom_specifications__tolerance",
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
					"Item Quality Inspection Parameter-acceptance_formula-description",
					"Quality Inspection Reading-acceptance_formula-description",
					"Quality Inspection-reference_type-options",
				],
			]
		],
	},
]
