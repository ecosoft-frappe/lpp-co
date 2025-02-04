// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Quality Inspection", {

	setup: function (frm) {
		frm.set_query("quality_inspection_template", function (doc) {
			return {
				filters: {
					custom_for_doctype: ["=", doc.reference_type],
				},
			};
		});
		// Override
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
		// Inspection Result HTML
		set_visual_inspection_html(frm)
		set_specification_inspection_html(frm)
		set_functional_testing_html(frm)
    },

    reference_type: function (frm) {
        if (frm.doc.reference_type === "Purchase Receipt") {
            frm.set_value("inspection_type", "Incoming");
        }
        else if (frm.doc.reference_type === "Job Card") {
            frm.set_value("inspection_type", "In Process");
        }
		else {
			frm.set_value("inspection_type", "");
		}
		// Generally, set blank for reference_name and item_code
		frm.set_value("reference_name", "");
		frm.set_value("quality_inspection_template", "");
    },

    reference_name: function (frm) {
		frm.set_value("item_code", "");
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

