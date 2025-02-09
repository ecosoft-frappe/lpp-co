frappe.ui.form.on("Material Request", {
	refresh: toggle_customer_reqd,
	material_request_type: function (frm) {
		toggle_customer_reqd(frm);
		if (frm.doc.material_request_type != "Manufacture") {
			frm.set_value("custom_sample_record", 0);
		}
	},
	custom_sample_record: function (frm) {
		if (frm.doc.custom_sample_record) {
			frm.set_value("material_request_type", "Manufacture");
		}
		toggle_customer_reqd(frm);
	},
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
	custom_plan_mold_creation: function (frm) {
		call_set_status(frm, "custom_plan_mold_creation", "custom_actual_mold_creation", "custom_status_mold_creation");
	},
	custom_actual_mold_creation: function (frm) {
		call_set_status(frm, "custom_plan_mold_creation", "custom_actual_mold_creation", "custom_status_mold_creation");
	},
	custom_plan_sample_production: function (frm) {
		call_set_status(frm, "custom_plan_sample_production", "custom_actual_sample_production", "custom_status_sample_production");
	},
	custom_actual_sample_production: function (frm) {
		call_set_status(frm, "custom_plan_sample_production", "custom_actual_sample_production", "custom_status_sample_production");
	},
	custom_plan_customer_delivery: function (frm) {
		call_set_status(frm, "custom_plan_customer_delivery", "custom_actual_customer_delivery", "custom_status_customer_delivery");
	},
	custom_actual_customer_delivery: function (frm) {
		call_set_status(frm, "custom_plan_customer_delivery", "custom_actual_customer_delivery", "custom_status_customer_delivery");
	},
});

function toggle_customer_reqd(frm) {
	frm.toggle_reqd("customer", (
		frm.doc.material_request_type == "Customer Provided" ||
		(frm.doc.material_request_type == "Manufacture" && frm.doc.custom_sample_record)
	));
}

function call_set_status(frm, plan, actual, status) {
	frappe.call({
		method: "lpp_co.custom.material_request.set_status",
		args: {
			plan: frm.doc[plan],
			actual: frm.doc[actual],
		},
		callback: function (r) {
			frm.set_value(status, r.message);
		},
	});
}
