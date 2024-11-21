import frappe

@frappe.whitelist()
def get_pending_approvals():
    # Fetch pending workflow actions excluding specific states
    attendance_adjustment = frappe.db.sql("""
        SELECT DISTINCT
            name AS "Document", 
            reference_name AS "Reference",
            reference_doctype AS "Document Type", 
            workflow_state AS "Workflow State" 
        FROM `tabWorkflow Action` t1
        WHERE NOT EXISTS (
            SELECT 1 
            FROM `tabWorkflow Action` t2
            WHERE t1.reference_name = t2.reference_name
            AND t2.workflow_state IN ("Approved", "For Approval", "Returned", "Checking Complete")
        )
    """, as_dict=True)
    return attendance_adjustment
    