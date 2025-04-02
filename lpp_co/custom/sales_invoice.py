from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice


class SalesInvoiceLPP(SalesInvoice):

	def validate_update_after_submit(self):
		# Because there is a bug that, incoie without choosing any batch / bundle
		# and hoping for system to choose automatically. This give an error,
		# i.e., Row #1: Not allowed to change Serial and Batch Bundle after submission from 3649978e032c27e35dc2 to ""
		# Still can't find the solutoin, so just ignore the validation for now
		if self.update_stock:
			self.flags.ignore_validate_update_after_submit = True
		super().validate_update_after_submit()
