import frappe

@frappe.whitelist()
def get_pending_approvals():
    results = []
    try:
        settings = frappe.get_single("Approval Setting")
        
        for i in settings.approval_setting_ct:
            document = i.document
            state = i.state
            
            document_check = frappe.get_all(document, filters={'workflow_state': state}, fields=['name'])
            
            for doc_info in document_check:
                doc = frappe.get_doc(document, doc_info['name'])
                doc_doctype = doc.doctype
                doc_docname = doc.name
                doc_workflow_state = doc.workflow_state
                
                # Append the data to results list
                results.append({
                    "Document": doc_docname,
                    "Reference": doc_docname,  # or the field you want to show as reference
                    "Document Type": doc_doctype,
                    "Workflow State": doc_workflow_state
                })
                
        # Return results for frontend
        return results
    
    except Exception as e:
        frappe.log_error(f"Error in get_pending_approvals: {str(e)}", "Pending Approvals")
