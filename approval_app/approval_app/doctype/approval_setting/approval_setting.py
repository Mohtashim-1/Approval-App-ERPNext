import frappe
from frappe.model.document import Document
from frappe import whitelist

class ApprovalSetting(Document):
    pass




@whitelist(allow_guest=True)
def get_doctype_meta(doctype):
    """
    Fetches the metadata of a doctype and returns it.
    """
    try:
        meta = frappe.get_meta(doctype)
        fields = [{'label': field.label, 'fieldname': field.fieldname} for field in meta.fields]
        return fields
    except Exception as e:
        frappe.log_error(f"Error fetching metadata for doctype: {doctype} - {str(e)}")
        return {'error': 'Failed to fetch metadata'}