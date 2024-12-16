import frappe

@frappe.whitelist()
def get_pending_approvals():
    results = []
    try:
        # Fetch the roles of the current user
        user_roles = frappe.get_roles(frappe.session.user)
        
        # Source 1: Fetch settings from the single doctype `Approval Setting`
        single_settings = frappe.get_doc("Approval Setting")
        if single_settings:
            for i in single_settings.approval_setting_ct:
                results.extend(fetch_documents(i, user_roles))
        
        # Source 2: Fetch settings from the normal doctype `Approval Settings`
        normal_settings = frappe.get_all(
            "Approval Settings",
            filters={"enabled": 1},  # Add a filter to fetch only enabled settings, if applicable
            fields=["name"]
        )
        
        for setting in normal_settings:
            normal_setting_doc = frappe.get_doc("Approval Settings", setting["name"])
            
            # Check if the current user has the required role for this setting
            if normal_setting_doc.role and normal_setting_doc.role in user_roles:
                for i in normal_setting_doc.approval_app_ct:
                    results.extend(fetch_documents(i, user_roles))
        
        # Return the results to the frontend
        return results

    except Exception as e:
        # Log any errors
        frappe.log_error(f"Error in get_pending_approvals: {str(e)}", "Pending Approvals")
        return {"error": "Failed to fetch pending approvals."}


def fetch_documents(setting_row, user_roles):
    """
    Fetch documents based on a single row of settings.
    """
    results = []
    try:
        document = setting_row.document  # Document type (e.g., "Sales Order")
        state = setting_row.state  # Workflow state (e.g., "Draft")
        field1_value = setting_row.field1  # Field name selected by the user
        
        # Fetch documents matching the workflow state
        document_check = frappe.get_all(
            document,
            filters={'workflow_state': state},
            fields=['name', 'creation']
        )
        
        for doc_info in document_check:
            doc = frappe.get_doc(document, doc_info['name'])
            doc_doctype = doc.doctype
            doc_docname = doc.name
            doc_workflow_state = doc.workflow_state
            doc_creation = doc_info['creation']

            # Dynamically fetch the value of the field selected in `field1`
            field_value = getattr(doc, field1_value, None) if field1_value else None

            # Fetch the latest comment for the document (optional)
            comment = frappe.db.get_value(
                "Communication",
                filters={
                    "reference_doctype": document,
                    "reference_name": doc_docname,
                    "communication_type": "Comment",
                },
                fieldname="content",
                order_by="creation desc"
            )

            # Append the data to the results list
            results.append({
                "Document": doc_docname,
                "Reference": doc_docname,  # Or the field you want to show as a reference
                "Document Type": doc_doctype,
                "Workflow State": doc_workflow_state,
                "Field Value": field_value,
                "Comments": comment if comment else "No Comments",
                "Creation Date": doc_creation
            })
    except Exception as e:
        frappe.log_error(f"Error in fetch_documents: {str(e)}", "Pending Approvals")
    
    return results
