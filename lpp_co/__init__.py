__version__ = "0.0.1"

# Monkey patching, to make search widget display in next lines
from .custom import search as lpp_search
from .custom import utils as lpp_utils
from .custom import reportview as lpp_reportview
from .custom import serial_batch_bundle as lpp_serial_batch_bundle
from frappe.desk import search as origin_search
from erpnext.buying import utils as origin_utils
from frappe.desk import reportview as origin_report_view
from erpnext.stock import serial_batch_bundle as origin_serial_batch_bundle

origin_search.search_widget = lpp_search.search_widget
origin_utils.validate_stock_item_warehouse = lpp_utils.validate_stock_item_warehouse
origin_report_view.export_query = lpp_reportview.export_query
origin_serial_batch_bundle.get_empty_batches_based_work_order = lpp_serial_batch_bundle.get_empty_batches_based_work_order

# Monkey patching for mobile pattern to accept any string
import re
from frappe import utils
utils.PHONE_NUMBER_PATTERN = re.compile(r".*")
