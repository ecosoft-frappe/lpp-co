// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

erpnext.selling.SalesOrderControllerLPP = class SalesOrderController extends erpnext.selling.SalesOrderController {
	// Override
	make_material_request() {
			frappe.model.open_mapped_doc({
			method: "lpp_co.custom.sales_order.make_material_request",
			frm: this.frm,
		});
	}
}
extend_cscript(cur_frm.cscript, new erpnext.selling.SalesOrderControllerLPP({ frm: cur_frm }));
