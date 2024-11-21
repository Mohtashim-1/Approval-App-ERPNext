# approval_app.py
import frappe

@frappe.whitelist()
def get_pending_approvals():
    # Make sure the query selects the columns you need
    attendance_adjustment = frappe.db.sql("""
        SELECT * FROM `tabAttendance Adjustment` 
        WHERE docstatus = 0  # This will only return records pending approval
    """, as_dict=True)  # Use as_dict=True to return results as a dictionary
    return attendance_adjustment
