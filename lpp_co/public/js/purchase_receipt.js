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
	// override_make_quality_inspection
	make_quality_inspection() {
		let data = [];
		const fields = [
			{
				label: "Items",
				fieldtype: "Table",
				fieldname: "items",
				cannot_add_rows: true,
				in_place_edit: true,
				data: data,
				get_data: () => {
					return data;
				},
				fields: [
					{
						fieldtype: "Data",
						fieldname: "docname",
						hidden: true
					},
					{
						fieldtype: "Read Only",
						fieldname: "item_code",
						label: __("Item Code"),
						in_list_view: true
					},
					{
						fieldtype: "Read Only",
						fieldname: "item_name",
						label: __("Item Name"),
						in_list_view: true
					},
					{
						fieldtype: "Float",
						fieldname: "qty",
						label: __("Accepted Quantity"),
						in_list_view: true,
						read_only: true
					},
					{
						fieldtype: "Float",
						fieldname: "sample_size",
						label: __("Sample Size"),
						hidden: true
					},
					{
						fieldtype: "Float",
						fieldname: "custom_qc_quantity",
						label: __("Packing Quantity"),
						in_list_view: true,
						reqd: true
					},
					{
						fieldtype: "Link",
						fieldname: "custom_qc_uom",
						label: __("Packing UOM"),
						options: "UOM",
						in_list_view: true
					},
					{
						fieldtype: "Data",
						fieldname: "description",
						label: __("Description"),
						hidden: true
					},
					{
						fieldtype: "Data",
						fieldname: "serial_no",
						label: __("Serial No"),
						hidden: true
					},
					{
						fieldtype: "Data",
						fieldname: "batch_no",
						label: __("Batch No"),
						hidden: true
					},
					{
						fieldtype: "Data",
						fieldname: "child_row_reference",
						label: __("Child Row Reference"),
						hidden: true
					}
				]
			}
		];

		const me = this;
		const dialog = new frappe.ui.Dialog({
			title: __("Select Items for Quality Inspection"),
			size: "extra-large",
			fields: fields,
			primary_action: function () {
				const data = dialog.get_values();
				const selected_data = data.items.filter(item => item?.__checked == 1 );
				frappe.call({
					method: "erpnext.controllers.stock_controller.make_quality_inspections",
					args: {
						doctype: me.frm.doc.doctype,
						docname: me.frm.doc.name,
						items: selected_data,
					},
					freeze: true,
					callback: function (r) {
						if (r.message.length > 0) {
							if (r.message.length === 1) {
								frappe.set_route("Form", "Quality Inspection", r.message[0]);
							} else {
								frappe.route_options = {
									"reference_type": me.frm.doc.doctype,
									"reference_name": me.frm.doc.name
								};
								frappe.set_route("List", "Quality Inspection");
							}
						}
						dialog.hide();
					}
				});
			},
			primary_action_label: __("Create")
		});

		frappe.call({
			method: "erpnext.controllers.stock_controller.check_item_quality_inspection",
			args: {
				doctype: this.frm.doc.doctype,
				items: this.frm.doc.items
			},
			freeze: true,
			callback: function (r) {
				r.message.forEach(item => {
					if (me.has_inspection_required(item)) {
						let dialog_items = dialog.fields_dict.items;
						dialog_items.df.data.push({
							"item_code": item.item_code,
							"item_name": item.item_name,
							"qty": item.qty,
							"description": item.description,
							"serial_no": item.serial_no,
							"batch_no": item.batch_no,
							"sample_size": item.sample_quantity,
							"child_row_reference": item.name,
						});
						dialog_items.grid.refresh();
					}
				});

				data = dialog.fields_dict.items.df.data;
				if (!data.length) {
					frappe.msgprint(__("All items in this document already have a linked Quality Inspection."));
				} else {
					dialog.show();
				}
			}
		});
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
							child_columns: ["item_code", "item_name", "description", "qty", "received_qty", "custom_balance_qty"],
						});
					},
					__("Get Items From")
				);
			}, 500);
		}
	}
})