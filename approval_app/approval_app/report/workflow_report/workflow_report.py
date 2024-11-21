# Copyright (c) 2024, mohtashim and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    query = """
        SELECT DISTINCT
            name AS "workflow_action_document", 
            reference_name AS "reference",
            reference_doctype AS "document_type", 
            workflow_state AS "status" 
        FROM `tabWorkflow Action` t1
        WHERE NOT EXISTS (
            SELECT 1 
            FROM `tabWorkflow Action` t2
            WHERE t1.reference_name = t2.reference_name
              AND (t2.workflow_state = "Approved" 
                   OR t2.workflow_state = "For Approval"
                   OR t2.workflow_state = "Returned"
                   OR t2.workflow_state = "Checking Complete")
        );
    """
    # Fetch data using the query
    data = frappe.db.sql(query, as_dict=True)

    # Define columns
    columns = [
        {"label": "Document", "fieldname": "workflow_action_document", "fieldtype": "Link", "options": "Workflow Action", "width": 200},
        {"label": "Reference No", "fieldname": "reference", "fieldtype": "Data", "width": 200},
        {"label": "Document Type", "fieldname": "document_type", "fieldtype": "Data", "width": 200},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 200},
    ]

    # Return the columns and data
    return columns, data
