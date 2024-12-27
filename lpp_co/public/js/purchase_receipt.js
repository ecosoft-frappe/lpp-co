// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.provide("lpp_co.stock");

lpp_co.stock.PurchaseReceiptController = class PurchaseReceiptController extends (
	erpnext.stock.PurchaseReceiptController
) {
	setup_quality_inspection() {
		const me = this;
		if (
			!this.frm.is_new() &&
			this.frm.doc.docstatus === 1 &&
			frappe.model.can_create("Quality Inspection")
		) {
			this.frm.add_custom_button(
				__("Quality Inspection(s)"),
				() => {
					me.make_quality_inspection();
				},
				__("Create")
			);
			this.frm.page.set_inner_btn_group_as_primary(__("Create"));
		}

		super.setup_quality_inspection();
	}
};

extend_cscript(cur_frm.cscript, new lpp_co.stock.PurchaseReceiptController({ frm: cur_frm }));
