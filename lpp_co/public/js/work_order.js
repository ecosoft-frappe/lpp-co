frappe.ui.form.on("Work Order", {
    refresh(frm) {               
        frm.remove_custom_button(__('Create Job Card'))
    },
});