erpnext.stock.StockEntryLPP = class StockEntryLPP extends erpnext.stock.StockEntry {
	set_default_account(company_fieldname, fieldname) {
		var me = this;

		return this.frm.call({
			method: "erpnext.accounts.utils.get_company_default",
			args: {
				fieldname: company_fieldname,
				company: this.frm.doc.company,
				ignore_validation: true
			},
			callback: function (r) {
				if (!r.exc) {
					$.each(me.frm.doc.items || [], function (i, d) {
						d[fieldname] = r.message;
					});
				}
			},
		});
	}
}

extend_cscript(cur_frm.cscript, new erpnext.stock.StockEntryLPP({ frm: cur_frm }));
