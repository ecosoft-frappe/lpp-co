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
		frm.set_value("custom_sample_record", 0)
	},
	custom_sample_record: function (frm) {
		frm.toggle_reqd("customer", (
			frm.doc.material_request_type == "Customer Provided" ||
			(frm.doc.material_request_type == "Manufacture" && frm.doc.custom_sample_record)
		));
	},

});