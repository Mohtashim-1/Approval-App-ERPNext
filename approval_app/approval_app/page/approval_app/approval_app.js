frappe.pages['approval-app'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Approval App',
        single_column: true
    });

    // Add the refresh button
    let $btn = page.set_secondary_action('Refresh', () => refresh(), 'octicon octicon-sync');

    // Function to refresh or reload data
    function refresh() {
        adj();  // Call the function that loads the pending approvals
    }

    // Function to fetch pending approvals via server-side method
    let adj = function() {
        frappe.call({
			method: "approval_app.approval_app.page.approval_app.approval_app.get_pending_approvals",  // Adjusted path
			callback: function(r) {
				if (r.message) {
					console.log("Pending Approvals:", r.message);
					// Handle the data here
				}
			}
		});
    };

    // Function to display pending approvals in the UI
    function display_approvals(data) {
		// Clear the page body
		page.body.empty();
	
		// Add a header
		let header = `<div class="form-group">
			<label for="search">Search Approvals:</label>
			<input type="text" id="search" class="form-control" placeholder="Search by name...">
		</div>`;
	
		// Create a table
		let table = `<table class="table table-bordered" id="approvals-table">
			<thead>
				<tr>
					<th>#</th>
					<th>Document Name</th>
					<th>Employee Name</th>
					<th>Status</th>
				</tr>
			</thead>
			<tbody>`;
	
		// Populate the table rows
		data.forEach((record, index) => {
			table += `<tr>
				<td>${index + 1}</td>
				<td>${record.name}</td>
				<td>${record.employee_name}</td>
				<td>${record.status || 'Pending'}</td>
			</tr>`;
		});
	
		table += `</tbody></table>`;
	
		// Add the header and table to the page body
		page.body.html(header + table);
	
		// Add search functionality
		document.getElementById('search').addEventListener('input', function() {
			let filter = this.value.toLowerCase();
			let rows = document.querySelectorAll('#approvals-table tbody tr');
			rows.forEach(row => {
				let text = row.textContent.toLowerCase();
				row.style.display = text.includes(filter) ? '' : 'none';
			});
		});
	}
};
