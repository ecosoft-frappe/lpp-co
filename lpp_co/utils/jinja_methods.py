import frappe
import math
import re


def get_company_info():
	try:
		# Get the Company Info data
		return frappe.get_doc("Company Info")
	except frappe.DoesNotExistError:
		# Log error if needed and return None
		# frappe.log_error("Company Info DocType does not exist", "get_company_info")
		return None
	except Exception:
		# Handle any other unexpected exceptions
		# frappe.log_error(f"Error retrieving Company Info: {e}", "get_company_info")
		return None


def chunk_list(lst: list, size):
	return [lst[i: i + size] for i in range(0, len(lst), size)]


def split_string(input_str, delimiter='-', index=None):
	# Split the input string by the specified delimiter and strip any leading/trailing whitespace from the parts
	parts = [part.strip() for part in input_str.split(delimiter)]

	# If index is provided, return the specific part, otherwise return the full list
	if index is not None and 0 <= index < len(parts):
		return parts[index]
	return parts


def calculate_qty(qty, custom_unit, per_page=8):
	"""
	Calculate qty based on custom_unit.
	If custom_unit is None or 0, return 0.
	If the result has a decimal part, round up to the nearest whole number.
	"""
	try:
		custom_unit = float(custom_unit or 0)  # Handle None or 0 in a single line
		qty = float(qty or 0)  # Handle None or empty qty in a single line
		if custom_unit == 0:
			return 0
		result = (qty / custom_unit) / per_page
		# Round up if there is a decimal part
		return math.ceil(result)
	except (ValueError, TypeError):
		return 0


def group_and_sum_by_po(docname):
	try:
		# Get the Sales Invoice document
		doc = frappe.get_doc("Sales Invoice", docname)

		# Safely get the taxes and default rate to 0 if not available
		taxes = doc.get("taxes", [])
		tax_rate = taxes[0].rate if taxes and hasattr(taxes[0], "rate") else 0

		grouped_amounts = {}

		# Iterate through the child table (items)
		for item in doc.items:
			# Check if the custom_po_no exists in the grouped_amounts dictionary
			if item.get("custom_po_no", "") not in grouped_amounts:
				grouped_amounts[item.get("custom_po_no", "")] = 0  # Initialize if not present

			# Add the amount to the corresponding custom_po_no
			grouped_amounts[item.get("custom_po_no", "")] += item.amount

		# Convert the result into an array of objects for Jinja
		result = []
		for po_no, amount in grouped_amounts.items():
			grand_total = (amount * tax_rate) / 100 + amount
			result.append({
				"po_no": po_no,
				"total_amount": amount,
				"grand_total": grand_total
			})

		return result

	except Exception as e:
		frappe.log_error(message=f"Error in group_and_sum_by_po: {str(e)}", title="Jinja Method Error")
		return []


def get_remark_form_items(account, id, item_table):
	item = frappe.db.get_all(
		item_table,
		filters={
			"expense_account": account,
			"parent": id,
		},
		fields=["custom_remark"],
		order_by="item_name asc"
	)

	# If no items are found, return '-'
	if not item:
		return "-"

	# Concatenate 'custom_remark' values
	remarks = ", ".join([i["custom_remark"] for i in item])

	return remarks


def sort_journal_entries(entries):
	def sort_key(entry):
		# Determine group based on debit and credit values
		if entry.debit_in_account_currency > 0 and entry.credit_in_account_currency == 0:
			group = 0  # Debit group
		elif entry.debit_in_account_currency == 0 and entry.credit_in_account_currency > 0:
			group = 1  # Credit group
		else:
			group = 2  # Invalid or mixed group
		# Return a tuple for sorting: (group, account)
		return (group, entry.account)

	# Sort the entries using the custom key
	return sorted(entries, key=sort_key)


def html_to_text_with_newlines_extended(html):
	"""
	Convert HTML to plain text with newlines for specific tags.

	Parameters:
		html (str): HTML content.

	Returns:
		str: Plain text with newlines.
	"""

	# Define tags that will be replaced with a newline
	newline_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "br"]

	# Replace opening and closing tags of newline_tags with a newline
	for tag in newline_tags:
		html = re.sub(fr"</?{tag}.*?>", "\n", html, flags=re.IGNORECASE)

	# Remove any remaining HTML tags
	plain_text = re.sub(r"<[^>]+>", "", html)

	# Normalize newlines (remove extra blank lines)
	plain_text = re.sub(r"\n+", "\n", plain_text).strip()

	return plain_text


def calculate_table_rows(text, table_width_px=200, font_size_px=11):
	"""
	Calculate the number of rows required to display text in a table.

	Parameters:
		text (str): The text to display.
		table_width_px (int): Width of the table in pixels. Default is 200.
		font_size_px (int): Font size in pixels. Default is 11.

	Returns:
		int: Number of rows required.
	"""
	avg_char_width_px = font_size_px/2
	chars_per_row = table_width_px // avg_char_width_px

	# Split the text into lines based on newlines
	lines = text.splitlines()

	# Calculate the total rows required
	total_rows = sum(-(-len(line) // chars_per_row) for line in lines)  # Ceiling division

	return total_rows


def paginate_items(items, max_rows_per_page=12, is_final=False, table_width_px=200, font_size_px=11):
	"""
	Paginate items based on the maximum number of rows per page.

	Parameters:
		items (list of dict): List of items, each containing 'item_name' and 'description'.
		max_rows_per_page (int): Maximum number of rows allowed per page. Default is 12.
		table_width_px (int): Table width in pixels. Default is 200.
		font_size_px (int): Font size in pixels. Default is 11.

	Returns:
		list of list of dict: Paginated items, each sublist represents a page.
	"""
	pages = []
	current_page = []
	current_rows = 0

	for item in items:
		# Ensure item_name and custom_descriptions are strings
		item_name = item.item_name or ""

		# Handle custom_descriptions based on 'final' flag
		if is_final and item != items[-1]:
			custom_descriptions = ""  # Ignore custom_descriptions for non-final items
		else:
			custom_descriptions = item.custom_descriptions or ""
			custom_descriptions = html_to_text_with_newlines_extended(custom_descriptions)


		# Combine item_name and custom_descriptions using dot notation
		combined_text = item_name + "\n" + custom_descriptions
		# Calculate rows required for this item
		rows_required = calculate_table_rows(combined_text, table_width_px, font_size_px)

		# Check if adding this item exceeds max rows per page
		if current_rows + rows_required > max_rows_per_page:
			# Start a new page
			pages.append(current_page)
			current_page = []
			current_rows = 0

		# Add item to the current page
		current_page.append(item)
		current_rows += rows_required

	# Add the last page if it has items
	if current_page:
		pages.append(current_page)

	return pages
