frappe.pages['approval-app'].on_page_load = function (wrapper) {
    // Ensure 'wrapper' is passed into the function correctly
    var page = frappe.ui.make_app_page({
        parent: wrapper,    // wrapper is used here
        title: 'Approval App',
        single_column: true,
    });

    let $btn = page.set_secondary_action('Refresh', () => refresh(), 'octicon octicon-sync');

    // Extract route parameters
    const route = frappe.get_route();
    const reference_doctype = route[1]; // Reference Doctype
    const reference_name = route[2]; // Reference Name

    // Function to refresh or reload data
    function refresh() {
        adj();
    }

    // Function to fetch pending approvals
    let adj = function () {
		frappe.call({
			method: 'approval_app.approval_app.page.approval_app.approval_app.get_pending_approvals',
			callback: function (r) {
				console.log(r);  // Add this to log the response
				if (r.message) {
					display_approvals(r.message);
				} else {
					console.error("No data returned from server.");
				}
			},
		});
	};

    // Function to display approvals
    function display_approvals(data) {
        page.body.empty();

        // Add a header
        let header = `<div class="form-group" style="display: flex; gap: 10px;">
            <label for="search">Search Approvals:</label>
            <input type="text" id="search" class="form-control" placeholder="Search by name...">

            <label for="search_doc">Search Document Type:</label>
            <input type="text" id="search_doc" class="form-control" placeholder="Search by Document Type...">

            <label for="search_state">Search Workflow State:</label>
            <input type="text" id="search_state" class="form-control" placeholder="Search by Workflow State...">
        </div>`;

        // Create a table
        let table = `<table class="table table-bordered" id="approvals-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Document Name</th>
                    <th>Reference Name</th>
                    <th>Document Type</th>
                    <th>Workflow State</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>`;

        // Populate the table rows
        data.forEach((record, index) => {
            let formatted_doc_type = record["Document Type"] ? record["Document Type"].toLowerCase().replace(/\s+/g, '-') : '';

            table += `<tr>
                <td>${index + 1}</td>
                <td>${record["Document"]}</td>
                <td>${record["Reference"]}</td>
                <td>${record["Document Type"]}</td>
                <td>${record["Workflow State"]}</td>
                 <td>
                    <a href="/app/${formatted_doc_type}/${record["Reference"]}" 
                    class="btn btn-primary btn-sm" 
                    target="_blank" 
                    rel="noopener noreferrer">Open Document</a>
                </td>
            </tr>`;
        });

        table += `</tbody></table>`;

        // Add the header and table to the page body
        page.body.html(header + table);

        // Add search functionality
        document.getElementById('search').addEventListener('input', function () {
            let filter = this.value.toLowerCase();
            let rows = document.querySelectorAll('#approvals-table tbody tr');
            rows.forEach(row => {
                let text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });

        document.getElementById('search_state').addEventListener('input', function () {
            let filter = this.value.toLowerCase();
            let rows = document.querySelectorAll('#approvals-table tbody tr');
            rows.forEach(row => {
                let text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });

        document.getElementById('search_doc').addEventListener('input', function () {
            let filter = this.value.toLowerCase();
            let rows = document.querySelectorAll('#approvals-table tbody tr');
            rows.forEach(row => {
                let text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }

    // Initial load
    adj();
};
