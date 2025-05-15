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

	make_purchase_invoice() {
		frappe.model.open_mapped_doc({
			method: "lpp_co.custom.purchase_receipt.make_purchase_invoice",
			frm: cur_frm,
		});
	}

};

extend_cscript(cur_frm.cscript, new lpp_co.stock.PurchaseReceiptController({ frm: cur_frm }));

frappe.ui.form.on("Purchase Receipt", {
	refresh(frm) {
		if (!frm.doc.is_return && frm.doc.status != "Closed" && frm.doc.docstatus == 0) {
			setTimeout(() => {
				frm.remove_custom_button(__("Purchase Order"), __("Get Items From"))
				frm.add_custom_button(
					__("Purchase Order"),
					function () {
						if (!frm.doc.supplier) {
							frappe.throw({
								title: __("Mandatory"),
								message: __("Please Select a Supplier"),
							});
						}
						erpnext.utils.map_current_doc({
							method: "lpp_co.custom.purchase_order.make_purchase_receipt",
							source_doctype: "Purchase Order",
							target: frm,
							setters: {
								supplier: frm.doc.supplier,
								schedule_date: undefined,
							},
							get_query_filters: {
								docstatus: 1,
								status: ["not in", ["Closed", "On Hold"]],
								per_received: ["<", 99.99],
								company: frm.doc.company,
							},
							allow_child_item_selection: true,
							child_fieldname: "items",
							child_columns: ["item_code", "item_name", "qty", "received_qty", "custom_balance_qty"],
						});
					},
					__("Get Items From")
				);
			}, 500);
		}
	}
})