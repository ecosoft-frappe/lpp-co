// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Quality Inspection", {

	// setup: function (frm) {
	// 	var original_set_query_item_code = frm.fields_dict["item_code"].get_query;
	// 	frm.set_query("item_code", function (doc) {
	// 		if (doc.reference_type === "Work Order") {
	// 			if (doc.reference_name) {
	// 				return {
	// 					query: "lpp_co.api.get_work_order_item",
	// 					filters: {
	// 						reference_type: doc.reference_type,
	// 						reference_name: doc.reference_name,
	// 					},
	// 				};
	// 			}
	// 		} else {
	// 			return original_set_query_item_code(doc);
	// 		}
	// 	});
	// },

	setup: function (frm) {
		// item code based on GRN/DN
		frm.set_query("item_code", function (doc) {
			let doctype = doc.reference_type;

			if (doc.reference_type !== "Job Card") {
				doctype =
					doc.reference_type == "Stock Entry" ? "Stock Entry Detail" : doc.reference_type + " Item";
			}

			if (doc.reference_type && doc.reference_name) {
				let filters = {
					from: doctype,
					inspection_type: doc.inspection_type,
				};

				if (doc.reference_type == doctype) filters["reference_name"] = doc.reference_name;
				else filters["parent"] = doc.reference_name;
				// Override with query from lpp_co module.
				return {
					query: "lpp_co.custom.quality_inspection.item_query",
					filters: filters,
				};
			}
		});

	},

    refresh: function(frm) {
		frm.set_query("custom_quality_inspection_type", function () {
			return {
				filters: {
					inspection_process: frm.doc.custom_quality_inspection_process,
					for_doctype: frm.doc.reference_type
				},
			};
		});
		// Inspection Result HTML
		set_visual_inspection_html(frm)
		set_specification_inspection_html(frm)
		set_functional_testing_html(frm)
    },

	// reference_name: function (frm) {
	// 	if (frm.doc.reference_type === "Work Order" && frm.doc.reference_name) {
	// 		frappe.db.get_value(
	// 			"Work Order",
	// 			{ name: frm.doc.reference_name },
	// 			"production_item",
	// 			(r) => {
	// 				frm.set_value("item_code", r.production_item);
	// 			}
	// 		);
	// 	}
	// },

	custom_quality_inspection_process: function(frm) {
		frm.set_value("custom_quality_inspection_type", "")
		frm.set_value("quality_inspection_template", "");
		// frm.set_value("custom_visual_inspection", "");
		// frm.set_value("custom_specification_inspection", "");
		// frm.set_value("custom_functional_testing", "");
	},

    custom_quality_inspection_type: function(frm) {
        const inspection_type = frm.doc.custom_quality_inspection_type;
        if (inspection_type) {
			frappe.db.get_doc("Quality Inspection Type", inspection_type).then((doc) => {
				frm.set_value({
					// custom_visual_inspection: doc.visual_inspection,
					// custom_specification_inspection: doc.specification_inspection,
					// custom_functional_testing: doc.functional_testing,
					quality_inspection_template: doc.quality_inspection_template
				});
			})
		}
    },

	custom_open_quality_inspection_result: function(frm) {
		open_quality_inspection_result(frm, "quality_inspection_template", "");
	},
	custom_open_visual_inspection: function(frm) {
		open_quality_inspection_result(frm, "quality_inspection_template", "Visual Inspection");
	},
	custom_open_specification_inspection: function(frm) {
		open_quality_inspection_result(frm, "quality_inspection_template", "Specification Inspection");
	},
	custom_open_functional_testing: function(frm) {
		open_quality_inspection_result(frm, "quality_inspection_template", "Functional Testing");
	},
	
});

function open_quality_inspection_result(frm, template_field, inspection_method) {
	frappe.set_route("List", "Quality Inspection Result", {
		quality_inspection: frm.doc.name,
		quality_inspection_template: frm.doc[template_field],
		inspection_method: inspection_method
	});
}

function set_visual_inspection_html(frm) {
	frappe.call({
		method: "get_visual_inspection_html",
		doc: frm.doc,
  		callback: (r) => {
			frm.get_field("custom_visual_inspection_html").$wrapper.html(r.message);
		},
	});
}

function set_specification_inspection_html(frm) {
	frappe.call({
		method: "get_specification_inspection_html",
		doc: frm.doc,
  		callback: (r) => {
			frm.get_field("custom_specification_inspection_html").$wrapper.html(r.message);
		},
	});
}

function set_functional_testing_html(frm) {
	frappe.call({
		method: "get_functional_testing_html",
		doc: frm.doc,
  		callback: (r) => {
			frm.get_field("custom_functional_testing_html").$wrapper.html(r.message);
		},
	});
}

