frappe.ui.form.MultiSelectDialog = class CustomMultiSelectDialog extends frappe.ui.form.MultiSelectDialog {
    init() {
        this.page_length = 20;
        this.child_page_length = 500;  // Override child_page_length
        this.fields = this.get_fields();

        this.make();

        this.selected_fields = new Set();
    }
}