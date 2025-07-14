import frappe
from erpnext.stock.serial_batch_bundle import get_batches_from_work_order
from erpnext.stock.serial_batch_bundle import get_batches_from_stock_entries
from erpnext.stock.serial_batch_bundle import set_batch_details_from_package


# Overwrite
def get_empty_batches_based_work_order(work_order, item_code):
    batches = get_batches_from_work_order(work_order, item_code)
    if not batches:
        return batches

    entries = get_batches_from_stock_entries(work_order, item_code)
    if not entries:
        return batches

    ids = [d.serial_and_batch_bundle for d in entries if d.serial_and_batch_bundle]
    if ids:
        set_batch_details_from_package(ids, batches)

    # Will be deprecated in v16
    for d in entries:
        if not d.batch_no:
            continue

        # LPP: Prevent deduct qty duplicate on batch
        if d.serial_and_batch_bundle:
            batch_no = frappe.get_all(
                "Serial and Batch Entry",
                filters={"parent": d.serial_and_batch_bundle, "is_outward": 0},
                pluck="batch_no"
            )
            if d.batch_no in batch_no:
                continue

        batches[d.batch_no] -= d.qty

    return batches
