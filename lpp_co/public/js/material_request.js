frappe.ui.form.on("Material Request", {

	// Make sure that customer is requried for Manufacture and Sample Record
	// But we have to incude the Customer Provided as per standard here
	refresh: function (frm) {
		frm.toggle_reqd("customer", (
			frm.doc.material_request_type == "Customer Provided" ||
			(frm.doc.material_request_type == "Manufacture" && frm.doc.custom_sample_record)
		))
	},
	material_request_type: function (frm) {
		frm.toggle_reqd("customer", (
			frm.doc.material_request_type == "Customer Provided" ||
			(frm.doc.material_request_type == "Manufacture" && frm.doc.custom_sample_record)
		));
		if (frm.doc.material_request_type != "Manufacture") {
			frm.set_value("custom_sample_record", 0)
		}
	},
	custom_sample_record: function (frm) {
		if (frm.doc.custom_sample_record) {
			frm.set_value("material_request_type", "Manufacture")
		}
		frm.toggle_reqd("customer", (
			frm.doc.material_request_type == "Customer Provided" ||
			(frm.doc.material_request_type == "Manufacture" && frm.doc.custom_sample_record)
		));
	},

	// Override, and change the method to lpp_co's
	get_items_from_sales_order: function (frm) {
		erpnext.utils.map_current_doc({
			method: "lpp_co.custom.sales_order.make_material_request",
			source_doctype: "Sales Order",
			target: frm,
			setters: {
				customer: frm.doc.customer || undefined,
				delivery_date: undefined,
			},
			get_query_filters: {
				docstatus: 1,
				status: ["not in", ["Closed", "On Hold"]],
				per_delivered: ["<", 99.99],
				company: frm.doc.company,
			},
		});
	},

});
