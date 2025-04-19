import flet as ft
import json
from datetime import datetime


def customers_view(page, app_bar, side_drawer):
    # Responsive sizing
    heading_size = 30 if page.width > 800 else 22
    subtext_size = 16 if page.width > 800 else 13
    padding_size = 30 if page.width > 800 else 15

    # Sample data - would be replaced with actual database in production
    sample_customers = [
        {"id": "C001", "name": "John Smith", "email": "john.smith@example.com", "phone": "555-123-4567",
         "address": "123 Main St, Anytown, USA", "type": "Regular", "since": "Jan 15, 2023"},
        {"id": "C002", "name": "Sarah Johnson", "email": "sarah.j@example.com", "phone": "555-234-5678",
         "address": "456 Oak Ave, Somecity, USA", "type": "Premium", "since": "Mar 3, 2022"},
        {"id": "C003", "name": "Michael Brown", "email": "mbrown@example.com", "phone": "555-345-6789",
         "address": "789 Pine Rd, Othertown, USA", "type": "Regular", "since": "Nov 20, 2023"},
        {"id": "C004", "name": "Emma Davis", "email": "emma.d@example.com", "phone": "555-456-7890",
         "address": "101 Elm Blvd, Newcity, USA", "type": "Premium", "since": "Jul 8, 2022"},
        {"id": "C005", "name": "Robert Wilson", "email": "rwilson@example.com", "phone": "555-567-8901",
         "address": "202 Cedar Ln, Oldtown, USA", "type": "Regular", "since": "Feb 12, 2023"},
    ]

    # State variables
    customers = sample_customers.copy()
    selected_customer = None
    edit_customer_id = None

    # Create data table rows from customers
    def create_customer_rows():
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(customer["id"])),
                    ft.DataCell(ft.Text(customer["name"])),
                    ft.DataCell(ft.Text(customer["email"])),
                    ft.DataCell(ft.Text(customer["phone"])),
                    ft.DataCell(ft.Text(customer["type"])),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color=ft.colors.BLUE,
                                tooltip="Edit",
                                on_click=lambda e, customer_id=customer["id"]: edit_customer(customer_id)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED,
                                tooltip="Delete",
                                on_click=lambda e, customer_id=customer["id"]: delete_customer(customer_id)
                            ),
                            ft.IconButton(
                                icon=ft.icons.INFO,
                                icon_color=ft.colors.AMBER,
                                tooltip="View Details",
                                on_click=lambda e, customer_id=customer["id"]: view_customer_details(customer_id)
                            )
                        ])
                    )
                ],
                selected=False,
                on_select_changed=lambda e, customer_id=customer["id"]: select_customer(customer_id, e.data == "true")
            ) for customer in customers
        ]

    # Helper function for email validation
    def validate_email(email):
        import re
        # Simple email validation pattern
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email)

    # Function to add customer - defined early to avoid reference issues
    def add_customer(e):
        # Validation for required fields
        if not customer_name_field.value:
            customer_name_field.error_text = "Name is required"
            page.update()
            return
        if not customer_email_field.value:
            customer_email_field.error_text = "Email is required"
            page.update()
            return
        elif not validate_email(customer_email_field.value):
            customer_email_field.error_text = "Please enter a valid email address"
            page.update()
            return
        if not customer_phone_field.value:
            customer_phone_field.error_text = "Phone number is required"
            page.update()
            return

        # Generate a new customer ID
        new_id = f"C{(len(customers) + 1):03d}"

        # Get current date for "since" field
        current_date = datetime.now().strftime("%b %d, %Y")

        # Create new customer
        new_customer = {
            "id": new_id,
            "name": customer_name_field.value,
            "email": customer_email_field.value,
            "phone": customer_phone_field.value,
            "address": customer_address_field.value,
            "type": customer_type_dropdown.value if customer_type_dropdown.value else "Regular",
            "since": current_date,
            "notes": customer_notes_field.value,
        }

        # Add to customers list
        customers.append(new_customer)

        # Update table
        customers_table.rows = create_customer_rows()

        # Close dialog and show success message
        add_customer_dialog.open = False
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Customer '{customer_name_field.value}' added successfully!"))
        page.snack_bar.open = True
        page.update()

    # Function to update a customer
    def update_customer(e):
        # Validation for required fields
        if not customer_name_field.value:
            customer_name_field.error_text = "Name is required"
            page.update()
            return
        if not customer_email_field.value:
            customer_email_field.error_text = "Email is required"
            page.update()
            return
        elif not validate_email(customer_email_field.value):
            customer_email_field.error_text = "Please enter a valid email address"
            page.update()
            return
        if not customer_phone_field.value:
            customer_phone_field.error_text = "Phone number is required"
            page.update()
            return

        # Find and update the customer
        for i, customer in enumerate(customers):
            if customer["id"] == edit_customer_id:
                # Preserve the original "since" date
                original_since = customer["since"]

                customers[i] = {
                    "id": edit_customer_id,
                    "name": customer_name_field.value,
                    "email": customer_email_field.value,
                    "phone": customer_phone_field.value,
                    "address": customer_address_field.value,
                    "type": customer_type_dropdown.value if customer_type_dropdown.value else "Regular",
                    "since": original_since,
                    "notes": customer_notes_field.value,
                }
                break

        # Update table
        customers_table.rows = create_customer_rows()

        # Close dialog and show success message
        add_customer_dialog.open = False
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Customer '{customer_name_field.value}' updated successfully!"))
        page.snack_bar.open = True
        page.update()

    # Header section
    header = ft.Container(
        padding=padding_size,
        content=ft.Column([
            ft.Text("Customer Management", size=heading_size),
            ft.Text("Add, edit, and manage your customers", size=subtext_size),
        ])
    )

    # Search and filter section
    search_field = ft.TextField(
        label="Search customers",
        prefix_icon=ft.icons.SEARCH,
        expand=True,
        on_change=lambda e: filter_customers(e.control.value)
    )

    filter_dropdown = ft.Dropdown(
        label="Customer Type",
        options=[
            ft.dropdown.Option("All Types"),
            ft.dropdown.Option("Regular"),
            ft.dropdown.Option("Premium"),
        ],
        value="All Types",
        width=200,
        on_change=lambda e: filter_by_type(e.control.value)
    )

    sort_dropdown = ft.Dropdown(
        label="Sort by",
        options=[
            ft.dropdown.Option("Name (A-Z)"),
            ft.dropdown.Option("Name (Z-A)"),
            ft.dropdown.Option("Most Recent"),
            ft.dropdown.Option("Oldest First"),
        ],
        value="Name (A-Z)",
        width=200,
        on_change=lambda e: sort_customers(e.control.value)
    )

    search_row = ft.Container(
        content=ft.ResponsiveRow([
            ft.Column([search_field], col={"sm": 12, "md": 6, "lg": 6}),
            ft.Column([
                ft.Row([filter_dropdown, sort_dropdown], spacing=10)
            ], col={"sm": 12, "md": 6, "lg": 6},
                horizontal_alignment=ft.CrossAxisAlignment.CENTER if page.width <= 800 else ft.CrossAxisAlignment.END)
        ]),
        padding=ft.padding.only(left=padding_size, right=padding_size, bottom=padding_size)
    )

    # Main customers table
    customers_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Phone")),
            ft.DataColumn(ft.Text("Type")),
            ft.DataColumn(ft.Text("Actions")),
        ],
        rows=create_customer_rows(),
        show_checkbox_column=True,
        heading_row_height=70,
        data_row_min_height=60,
        data_row_max_height=80,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
    )

    # Wrap the table in a scrollable container for mobile view
    customers_table_container = ft.Container(
        content=ft.Column([
            # Hint text for mobile users about horizontal scrolling
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.SWIPE, color=ft.colors.GREY_500, size=16),
                    ft.Text("Scroll horizontally to see more", color=ft.colors.GREY_500, size=12),
                ], spacing=5),
                visible=page.width <= 800,
                padding=ft.padding.only(bottom=10),
                alignment=ft.alignment.center_right,
            ),
            # Use a ScrollableControl for horizontal scrolling
            ft.Row(
                [customers_table],
                scroll=ft.ScrollMode.ALWAYS if page.width <= 800 else ft.ScrollMode.AUTO,
                auto_scroll=False,
            )
        ]),
        padding=ft.padding.only(left=padding_size, right=padding_size, bottom=padding_size),
    )

    # Form fields for customer dialogs
    customer_name_field = ft.TextField(label="Customer Name", autofocus=True)
    customer_email_field = ft.TextField(label="Email Address")
    customer_phone_field = ft.TextField(label="Phone Number")
    customer_address_field = ft.TextField(label="Address", multiline=True, min_lines=2, max_lines=3)
    customer_type_dropdown = ft.Dropdown(
        label="Customer Type",
        options=[
            ft.dropdown.Option("Regular"),
            ft.dropdown.Option("Premium"),
        ],
        value="Regular",  # Default value set
    )
    customer_notes_field = ft.TextField(label="Notes (Optional)", multiline=True, min_lines=2, max_lines=4)

    # Add customer dialog
    add_customer_dialog = ft.AlertDialog(
        title=ft.Text("Add New Customer"),
        content=ft.Column([
            customer_name_field,
            customer_email_field,
            customer_phone_field,
            customer_address_field,
            customer_type_dropdown,
            customer_notes_field,
        ], height=400, width=500, scroll=ft.ScrollMode.AUTO),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(add_customer_dialog)),
            ft.TextButton("Add", on_click=add_customer),  # Now the reference should work
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Summary cards with properly centered values
    summary_cards = ft.ResponsiveRow([
        ft.Container(
            col={"sm": 6, "md": 3, "lg": 3},
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.PEOPLE, color=ft.colors.BLUE_500),
                    ft.Text("Total Customers", color=ft.colors.GREY_700, size=subtext_size),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Text(str(len(customers)),
                                    size=heading_size,
                                    text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    width=float('inf')
                ),
            ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15),
        ),
        ft.Container(
            col={"sm": 6, "md": 3, "lg": 3},
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.STAR, color=ft.colors.AMBER_500),
                    ft.Text("Premium Customers", color=ft.colors.GREY_700, size=subtext_size),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Text(str(sum(1 for c in customers if c['type'] == "Premium")),
                                    size=heading_size,
                                    text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    width=float('inf')
                ),
            ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15),
        ),
        ft.Container(
            col={"sm": 6, "md": 3, "lg": 3},
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.PERSON, color=ft.colors.GREEN_500),
                    ft.Text("Regular Customers", color=ft.colors.GREY_700, size=subtext_size),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Text(str(sum(1 for c in customers if c['type'] == "Regular")),
                                    size=heading_size,
                                    text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    width=float('inf')
                ),
            ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15),
        ),
        ft.Container(
            col={"sm": 6, "md": 3, "lg": 3},
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.NEW_RELEASES, color=ft.colors.PURPLE_500),
                    ft.Text("New This Month", color=ft.colors.GREY_700, size=subtext_size),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Text("2",  # This would be calculated based on actual dates
                                    size=heading_size,
                                    text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    width=float('inf')
                ),
            ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15),
        ),
    ])

    # Action buttons
    def open_add_dialog(e):
        # Clear the fields for new input
        customer_name_field.value = ""
        customer_email_field.value = ""
        customer_phone_field.value = ""
        customer_address_field.value = ""
        customer_type_dropdown.value = "Regular"
        customer_notes_field.value = ""

        # Clear any error messages
        customer_name_field.error_text = None
        customer_email_field.error_text = None
        customer_phone_field.error_text = None

        # Set dialog to add customer
        add_customer_dialog.title = ft.Text("Add New Customer")
        add_customer_dialog.actions = [
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(add_customer_dialog)),
            ft.TextButton("Add", on_click=add_customer),
        ]

        page.dialog = add_customer_dialog
        add_customer_dialog.open = True
        page.update()



    def view_customer_details(customer_id):
        # Find the customer
        customer = next((c for c in customers if c["id"] == customer_id), None)

        if customer:
            details_dialog = ft.AlertDialog(
                title=ft.Text(f"Customer Details: {customer['name']}"),
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.BADGE),
                        title=ft.Text("Customer ID"),
                        subtitle=ft.Text(customer["id"]),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.EMAIL),
                        title=ft.Text("Email"),
                        subtitle=ft.Text(customer["email"]),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.PHONE),
                        title=ft.Text("Phone"),
                        subtitle=ft.Text(customer["phone"]),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.HOME),
                        title=ft.Text("Address"),
                        subtitle=ft.Text(customer["address"]),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.STAR if customer["type"] == "Premium" else ft.icons.PERSON),
                        title=ft.Text("Customer Type"),
                        subtitle=ft.Text(customer["type"]),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.CALENDAR_TODAY),
                        title=ft.Text("Customer Since"),
                        subtitle=ft.Text(customer["since"]),
                    ),
                ], tight=True, spacing=5, scroll=ft.ScrollMode.AUTO, width=400, height=350),
                actions=[
                    ft.TextButton("Close", on_click=lambda e: close_dialog(details_dialog)),
                    ft.TextButton("Edit", on_click=lambda e: edit_from_details(customer_id, details_dialog)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            page.dialog = details_dialog
            details_dialog.open = True
            page.update()

    def edit_from_details(customer_id, details_dialog):
        # Close details dialog and open edit dialog
        close_dialog(details_dialog)
        edit_customer(customer_id)

    def import_customers(e):
        # In a real app, this would open a file picker
        # For now, we'll simulate import with a notification
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Customer import feature would open a file picker in a real app."),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()

    export_dialog = ft.AlertDialog(
        title=ft.Text("Export Customer Data"),
        content=ft.Column([
            ft.Text("Choose export format:"),
            ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.icons.FILE_PRESENT),
                        ft.Text("CSV"),
                    ]),
                    on_click=lambda e: export_csv(),
                ),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.icons.FILE_PRESENT),
                        ft.Text("JSON"),
                    ]),
                    on_click=lambda e: export_json(),
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], width=400, tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(export_dialog)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_export_dialog(e):
        page.dialog = export_dialog
        export_dialog.open = True
        page.update()

    preview_dialog_csv = ft.AlertDialog()

    def export_csv():
        # In a real app, this would save the file to disk
        # For now, we'll simulate successful export

        # Create CSV content as string
        csv_content = "ID,Name,Email,Phone,Address,Type,Since\n"
        for customer in customers:
            csv_content += f"{customer['id']},{customer['name']},{customer['email']},{customer['phone']},\"{customer['address']}\",{customer['type']},{customer['since']}\n"

        # Show confirmation with preview
        global preview_dialog_csv
        preview_dialog_csv = ft.AlertDialog(
            title=ft.Text("Export Preview"),
            content=ft.Column([
                ft.Text("CSV data generated successfully. Here's a preview:"),
                ft.Container(
                    content=ft.Text(csv_content[:200] + "..." if len(csv_content) > 200 else csv_content),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    border_radius=5,
                    padding=10,
                ),
                ft.Text("In a complete app, this would be saved to a file."),
            ], width=400, height=200, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Close", on_click=lambda e: close_dialog(preview_dialog_csv)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Close export dialog and show preview
        page.dialog.open = False
        page.dialog = preview_dialog_csv
        preview_dialog_csv.open = True

        # Show success notification
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Customer data exported successfully to CSV!"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()

    def export_json():
        # Convert customers to JSON string
        json_content = json.dumps(customers, indent=2)

        # Show confirmation with preview
        preview_dialog = ft.AlertDialog(
            title=ft.Text("Export Preview"),
            content=ft.Column([
                ft.Text("JSON data generated successfully. Here's a preview:"),
                ft.Container(
                    content=ft.Text(json_content[:200] + "..." if len(json_content) > 200 else json_content),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    border_radius=5,
                    padding=10,
                ),
                ft.Text("In a complete app, this would be saved to a file."),
            ], width=400, height=200, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Close", on_click=lambda e: close_dialog(preview_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Close export dialog and show preview
        page.dialog.open = False
        page.dialog = preview_dialog
        preview_dialog.open = True

        # Show success notification
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Customer data exported successfully to JSON!"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()

    action_buttons = ft.Container(
        content=ft.Row([
            ft.ElevatedButton(
                "Add Customer",
                icon=ft.icons.PERSON_ADD,
                on_click=open_add_dialog,
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
            ),
            ft.ElevatedButton(
                "Import",
                icon=ft.icons.UPLOAD_FILE,
                on_click=import_customers,
                bgcolor=ft.colors.GREEN,
                color=ft.colors.WHITE,
            ),
            ft.ElevatedButton(
                "Export Data",
                icon=ft.icons.DOWNLOAD,
                on_click=open_export_dialog,
            ),
        ], spacing=7, wrap=True,
            alignment=ft.MainAxisAlignment.CENTER),
        padding=padding_size // 4,
    )

    # Helper functions
    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def select_customer(customer_id, selected):
        for row in customers_table.rows:
            if row.cells[0].content.value == customer_id:
                row.selected = selected
        page.update()

    def edit_customer(customer_id):
        # Find the customer
        global edit_customer_id
        edit_customer_id = customer_id

        # Find the customer data
        for customer in customers:
            if customer["id"] == customer_id:
                # Fill the form with customer data
                customer_name_field.value = customer["name"]
                customer_email_field.value = customer["email"]
                customer_phone_field.value = customer["phone"]
                customer_address_field.value = customer["address"]
                customer_type_dropdown.value = customer["type"]
                customer_notes_field.value = customer.get("notes", "")

                # Clear any error messages
                customer_name_field.error_text = None
                customer_email_field.error_text = None
                customer_phone_field.error_text = None

                # Set dialog to edit mode
                add_customer_dialog.title = ft.Text(f"Edit Customer: {customer['name']}")
                add_customer_dialog.actions = [
                    ft.TextButton("Cancel", on_click=lambda e: close_dialog(add_customer_dialog)),
                    ft.TextButton("Update", on_click=update_customer),
                ]

                # Show the dialog
                page.dialog = add_customer_dialog
                add_customer_dialog.open = True
                page.update()
                break

    def delete_customer(customer_id):
        # Find the customer to get the name for the confirmation message
        customer = next((c for c in customers if c["id"] == customer_id), None)
        if not customer:
            return

        # Create confirmation dialog
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirm Deletion"),
            content=ft.Text(
                f"Are you sure you want to delete customer '{customer['name']}'? This action cannot be undone."),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog(confirm_dialog)),
                ft.TextButton("Delete", on_click=lambda e: confirm_delete_customer(customer_id, confirm_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    def confirm_delete_customer(customer_id, confirm_dialog):
        # Close the confirmation dialog
        close_dialog(confirm_dialog)

        # Find and remove the customer
        for i, customer in enumerate(customers):
            if customer["id"] == customer_id:
                customers.pop(i)
                customers_table.rows = create_customer_rows()
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Customer deleted successfully"))
                page.snack_bar.open = True
                page.update()
                break

    def filter_customers(search_text):
        # Filter customers based on search text
        if not search_text:
            customers_table.rows = create_customer_rows()
        else:
            search_text = search_text.lower()
            filtered_rows = []

            for row in create_customer_rows():
                customer_id = row.cells[0].content.value
                customer = next((c for c in customers if c["id"] == customer_id), None)

                if (customer and (
                        search_text in customer["name"].lower() or
                        search_text in customer["email"].lower() or
                        search_text in customer["phone"].lower() or
                        search_text in customer["address"].lower()
                )):
                    filtered_rows.append(row)

            customers_table.rows = filtered_rows
        page.update()

    def filter_by_type(customer_type):
        if customer_type == "All Types":
            customers_table.rows = create_customer_rows()
        else:
            filtered_customers = [c for c in customers if c["type"] == customer_type]
            customers_table.rows = [
                row for row in create_customer_rows()
                if row.cells[0].content.value in [c["id"] for c in filtered_customers]
            ]
        page.update()

    def sort_customers(sort_option):
        sorted_customers = customers.copy()

        if sort_option == "Name (A-Z)":
            sorted_customers.sort(key=lambda c: c["name"])
        elif sort_option == "Name (Z-A)":
            sorted_customers.sort(key=lambda c: c["name"], reverse=True)
        elif sort_option == "Most Recent":
            # In a real app, you would parse the dates properly
            # For this demo, we'll sort by ID in reverse (assuming higher IDs are newer)
            sorted_customers.sort(key=lambda c: c["id"], reverse=True)
        elif sort_option == "Oldest First":
            # Sort by ID (assuming lower IDs are older)
            sorted_customers.sort(key=lambda c: c["id"])

        customers_table.rows = [
            row for c in sorted_customers
            for row in create_customer_rows()
            if row.cells[0].content.value == c["id"]
        ]
        page.update()

    # Update UI based on window resize
    def on_resize(e):
        # Update responsive elements based on new width
        is_mobile = page.width <= 800

        # Adjust table scroll mode
        customers_table_container.content.controls[0].visible = is_mobile
        customers_table_container.content.controls[1].scroll = ft.ScrollMode.ALWAYS if is_mobile else ft.ScrollMode.AUTO

        # Adjust button layout
        action_buttons.content.alignment = ft.MainAxisAlignment.CENTER if page.width <= 600 else ft.MainAxisAlignment.START

        # Update header and text sizes
        nonlocal heading_size, subtext_size, padding_size
        heading_size = 30 if page.width > 800 else 22
        subtext_size = 16 if page.width > 800 else 13
        padding_size = 30 if page.width > 800 else 15

        header.content.controls[0].size = heading_size
        header.content.controls[1].size = subtext_size

        # Update summary cards
        for card in summary_cards.controls:
            card.padding = padding_size
            card.content.controls[0].controls[1].size = subtext_size
            card.content.controls[1].content.size = heading_size

        page.update()

    page.on_resize = on_resize
    page.drawer = side_drawer

    # Create a container for customers segmentation (would be connected to a real chart in production)
    segmentation_chart = ft.Container(
        content=ft.Column([
            ft.Text("Customer Segmentation", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        width=150,
                        height=150,
                        border_radius=75,
                        bgcolor=ft.colors.BLUE_100,
                        content=ft.Stack([
                            ft.Container(
                                width=100,
                                height=100,
                                border_radius=50,
                                bgcolor=ft.colors.BLUE_400,
                                alignment=ft.alignment.center,
                                content=ft.Text("60%", color=ft.colors.WHITE, size=20, weight=ft.FontWeight.BOLD),
                            ),
                        ]),
                        alignment=ft.alignment.center,
                    ),
                    ft.Column([
                        ft.Container(
                            content=ft.Row([
                                ft.Container(width=20, height=20, bgcolor=ft.colors.BLUE_400),
                                ft.Text("Regular Customers (60%)", size=16),
                            ], spacing=10),
                            margin=10,
                        ),
                        ft.Container(
                            content=ft.Row([
                                ft.Container(width=20, height=20, bgcolor=ft.colors.BLUE_100),
                                ft.Text("Premium Customers (40%)", size=16),
                            ], spacing=10),
                            margin=10,
                        ),
                    ]),
                ], alignment=ft.MainAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                margin=20,
            ),
            ft.Text("This is a static visualization. In a real app, this would be an interactive chart.",
                    italic=True, size=12, color=ft.colors.GREY_600),
        ]),
        padding=20,
        margin=10,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
    )

    # Container for customer acquisition timeline (would be a real chart in production)
    acquisition_chart = ft.Container(
        content=ft.Column([
            ft.Text("Customer Acquisition Timeline", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(width=50, content=ft.Text("5", text_align=ft.TextAlign.RIGHT)),
                        ft.Container(
                            expand=True,
                            height=20,
                            bgcolor=ft.colors.GREEN_500,
                            border_radius=5,
                        ),
                    ]),
                    ft.Row([
                        ft.Container(width=50, content=ft.Text("3", text_align=ft.TextAlign.RIGHT)),
                        ft.Container(
                            expand=True,
                            height=20,
                            bgcolor=ft.colors.GREEN_400,
                            border_radius=5,
                            width=150,
                        ),
                    ]),
                    ft.Row([
                        ft.Container(width=50, content=ft.Text("2", text_align=ft.TextAlign.RIGHT)),
                        ft.Container(
                            expand=True,
                            height=20,
                            bgcolor=ft.colors.GREEN_300,
                            border_radius=5,
                            width=100,
                        ),
                    ]),
                    ft.Row([
                        ft.Container(width=50, content=ft.Text("4", text_align=ft.TextAlign.RIGHT)),
                        ft.Container(
                            expand=True,
                            height=20,
                            bgcolor=ft.colors.GREEN_200,
                            border_radius=5,
                            width=200,
                        ),
                    ]),
                    ft.Row([
                        ft.Container(width=50, content=ft.Text("1", text_align=ft.TextAlign.RIGHT)),
                        ft.Container(
                            expand=True,
                            height=20,
                            bgcolor=ft.colors.GREEN_100,
                            border_radius=5,
                            width=50,
                        ),
                    ]),
                    ft.Row([
                        ft.Container(width=50),
                        ft.Row([
                            ft.Text("Jan"),
                            ft.Text("Feb"),
                            ft.Text("Mar"),
                            ft.Text("Apr"),
                            ft.Text("May"),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True),
                    ]),
                ], spacing=10),
                padding=20,
            ),
            ft.Text("This is a static visualization. In a real app, this would be an interactive chart.",
                    italic=True, size=12, color=ft.colors.GREY_600),
        ]),
        padding=20,
        margin=10,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
    )

    # Customer insights section
    insights_section = ft.Container(
        content=ft.ResponsiveRow([
            ft.Column([segmentation_chart], col={"sm": 12, "md": 6, "lg": 6}),
            ft.Column([acquisition_chart], col={"sm": 12, "md": 6, "lg": 6}),
        ]),
        padding=ft.padding.only(left=padding_size, right=padding_size),
    )

    # Bring it all together
    return ft.View(
        route="/customers",
        appbar=app_bar,
        controls=[
            side_drawer,
            header,
            summary_cards,
            action_buttons,
            search_row,
            customers_table_container,
            insights_section,
            add_customer_dialog,
            export_dialog
        ],
        scroll=ft.ScrollMode.AUTO
    )