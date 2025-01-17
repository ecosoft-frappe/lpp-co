import frappe


def execute():
	types = [
		("IMQA - Agent & Others", "IMQA", "Purchase Receipt"),
		("IMQA - Plastic Pellets", "IMQA", "Purchase Receipt"),
		("IMQA - Plastic Sheet", "IMQA", "Purchase Receipt"),
		("Buyoff - Reel", "Buyoff", "Job Card"),
		("Buyoff - Tray (CUT)", "Buyoff", "Job Card"),
		("Buyoff - Tray (VAC)", "Buyoff", "Job Card"),
		("Roving - Reel", "Roving", "Job Card"),
		("Roving - Tray", "Roving", "Job Card"),
		("Final Inspection - Reel", "Final Inspection", "Job Card"),
		("Final Inspection - Tray", "Final Inspection", "Job Card"),
	]
	for type in types:
		if frappe.db.exists("Quality Inspection Type", type[0]):
			continue
		doc = frappe.new_doc("Quality Inspection Type")
		doc.inspection_type = type[0]
		doc.inspection_process = type[1]
		doc.for_doctype = type[2]
		doc.insert(ignore_permissions=True)
	return