__version__ = "0.0.1"

# Monkey patching, to make search widget display in next lines
from .custom import search as lpp_search
from .custom import utils as lpp_utils
from frappe.desk import search as origin_search
from erpnext.buying import utils as origin_utils

origin_search.search_widget = lpp_search.search_widget
origin_utils.validate_stock_item_warehouse = lpp_utils.validate_stock_item_warehouse

# Monkey patching for mobile pattern to accept any string
import re
from frappe import utils
utils.PHONE_NUMBER_PATTERN = re.compile(r".*")
