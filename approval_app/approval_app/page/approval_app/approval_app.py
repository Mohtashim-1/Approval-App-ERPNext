import frappe

@frappe.whitelist()
def get_pending_approvals():
    results = []
    try:
        settings = frappe.get_single("Approval Setting")
        
        for i in settings.approval_setting_ct:
            document = i.document  # Document type (e.g., "Sales Order")
            state = i.state  # Workflow state (e.g., "Draft")
            field1_value = i.field1  # The field name selected by the user
            
            # Fetch documents matching the workflow state
            document_check = frappe.get_all(document, filters={'workflow_state': state}, fields=['name', 'creation'])
            
            for doc_info in document_check:
                doc = frappe.get_doc(document, doc_info['name'])
                doc_doctype = doc.doctype
                doc_docname = doc.name
                doc_workflow_state = doc.workflow_state
                doc_creation = doc_info['creation']
                
                # Dynamically get the value of the field selected in field1
                field_value = getattr(doc, field1_value, None) if field1_value else None
                
                # Append the data to results list
                results.append({
                    "Document": doc_docname,
                    "Reference": doc_docname,  # Or the field you want to show as reference
                    "Document Type": doc_doctype,
                    "Workflow State": doc_workflow_state,
                    "Field Value": field_value,
                    "Creation Date": doc_creation  # Add creation date to results
                })
        
        # Return results for frontend
        return results

    except Exception as e:
        frappe.log_error(f"Error in get_pending_approvals: {str(e)}", "Pending Approvals")
        return {"error": "Failed to fetch pending approvals."}
