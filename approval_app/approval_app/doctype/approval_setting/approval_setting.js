frappe.ui.form.on("Approval Setting", {
    refresh: function(frm) {
        // Replace 'approval_setting_ct' with your actual child table name
        var child_table = "approval_setting_ct"; 
        var fieldname = "field1";  // The field in the child table to populate
        var document_field = "document";  // The field in the child table that stores the document reference
        
        // Loop through the child table rows
        $.each(frm.fields_dict[child_table].grid.grid_rows_by_docname, function(cdn, row) {
            // Get the referenced document value from the child table row
            var document_value = row.doc[document_field];
            
            if (document_value) {
                // Call the whitelisted function to fetch fields for the referenced doctype
                frappe.call({
                    method: "approval_app.approval_app.doctype.approval_setting.approval_setting.get_doctype_meta",  // Your method path
                    args: {
                        doctype: document_value
                    },
                    callback: function(response) {
                        if (response.message && response.message.length > 0) {
                            // Extract field names from the response
                            var fieldnames = response.message.map(function(doc) {
                                return doc.fieldname;
                            });
                            
                            // Set the options of field1 to the list of fieldnames
                            var field = frappe.utils.filter_dict(row.docfields, { "fieldname": fieldname })[0];
                            
                            if (field) {
                                field.options = fieldnames;  // Update options with the field names
                                frm.refresh_field(child_table);  // Refresh the form to reflect the changes
                            }
                        } else {
                            frappe.msgprint("No fields found for the specified document.");
                        }
                    },
                    error: function(error) {
                        frappe.msgprint("Error fetching fields: " + error.message);
                    }
                });
            }
        });
    }
});
