import flet as ft
import random
import time
import json
from datetime import datetime


def inventory_view(page, app_bar, side_drawer):
    heading_size = 30 if page.width > 800 else 22
    subtext_size = 16 if page.width > 800 else 13
    padding_size = 30 if page.width > 800 else 15

    # Sample data - would be replaced with actual database in production
    sample_products = [
        {"id": "P001", "name": "Premium Coffee Beans", "category": "Beverages", "price": 14.99, "stock": 45,
         "barcode": "8901234567890"},
        {"id": "P002", "name": "Organic Green Tea", "category": "Beverages", "price": 9.99, "stock": 32,
         "barcode": "7890123456789"},
        {"id": "P003", "name": "Whole Wheat Bread", "category": "Bakery", "price": 4.50, "stock": 18,
         "barcode": "6789012345678"},
        {"id": "P004", "name": "Fresh Apples (1kg)", "category": "Produce", "price": 3.99, "stock": 60,
         "barcode": "5678901234567"},
        {"id": "P005", "name": "Chocolate Cookies", "category": "Snacks", "price": 5.75, "stock": 24,
         "barcode": "4567890123456"},
    ]

    # State variables
    products = sample_products.copy()
    selected_product = None

    # Function to get product by barcode
    def get_product_by_barcode(barcode):
        for product in products:
            if product["barcode"] == barcode:
                return product
        return None

    # Create data table rows from products
    def create_product_rows():
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(product["id"])),
                    ft.DataCell(ft.Text(product["name"])),
                    ft.DataCell(ft.Text(product["category"])),
                    ft.DataCell(ft.Text(f"${product['price']:.2f}")),
                    ft.DataCell(ft.Text(str(product["stock"]))),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color=ft.colors.BLUE,
                                tooltip="Edit",
                                on_click=lambda e, product_id=product["id"]: edit_product(product_id)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED,
                                tooltip="Delete",
                                on_click=lambda e, product_id=product["id"]: delete_product(product_id)
                            )
                        ])
                    )
                ],
                selected=False,
                on_select_changed=lambda e, product_id=product["id"]: select_product(product_id, e.data == "true")
            ) for product in products
        ]

    # Header section
    header = ft.Container(
        padding=padding_size,
        content=ft.Column([
            ft.Text("Inventory Management", size=heading_size),
            ft.Text("Add, edit, and manage your products", size=subtext_size),
        ])
    )

    # Search and filter section
    search_field = ft.TextField(
        label="Search products",
        prefix_icon=ft.icons.SEARCH,
        expand=True,
        on_change=lambda e: filter_products(e.control.value)
    )

    filter_dropdown = ft.Dropdown(
        label="Category",
        options=[
            ft.dropdown.Option("All Categories"),
            ft.dropdown.Option("Beverages"),
            ft.dropdown.Option("Bakery"),
            ft.dropdown.Option("Produce"),
            ft.dropdown.Option("Snacks"),
        ],
        value="All Categories",
        width=200,
        on_change=lambda e: filter_by_category(e.control.value)
    )

    sort_dropdown = ft.Dropdown(
        label="Sort by",
        options=[
            ft.dropdown.Option("Name (A-Z)"),
            ft.dropdown.Option("Name (Z-A)"),
            ft.dropdown.Option("Price (Low-High)"),
            ft.dropdown.Option("Price (High-Low)"),
            ft.dropdown.Option("Stock (Low-High)"),
        ],
        value="Name (A-Z)",
        width=200,
        on_change=lambda e: sort_products(e.control.value)
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

    # Main products table
    products_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Product Name")),
            ft.DataColumn(ft.Text("Category")),
            ft.DataColumn(ft.Text("Price")),
            ft.DataColumn(ft.Text("Stock")),
            ft.DataColumn(ft.Text("Actions")),
        ],
        rows=create_product_rows(),
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
    products_table_container = ft.Container(
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
                [products_table],
                scroll=ft.ScrollMode.ALWAYS if page.width <= 800 else ft.ScrollMode.AUTO,
                auto_scroll=False,
            )
        ]),
        padding=ft.padding.only(left=padding_size, right=padding_size, bottom=padding_size),
    )

    # Form fields for product dialogs (shared between add and edit)
    product_name_field = ft.TextField(label="Product Name", autofocus=True)
    product_category_dropdown = ft.Dropdown(
        label="Category",
        options=[
            ft.dropdown.Option("Beverages"),
            ft.dropdown.Option("Bakery"),
            ft.dropdown.Option("Produce"),
            ft.dropdown.Option("Snacks"),
            ft.dropdown.Option("Other"),
        ],
    )
    product_price_field = ft.TextField(label="Price ($)", keyboard_type=ft.KeyboardType.NUMBER)
    product_stock_field = ft.TextField(label="Stock", keyboard_type=ft.KeyboardType.NUMBER)
    product_barcode_field = ft.TextField(label="Barcode (Optional)")

    # Variable to track the product ID during editing
    edit_product_id = None

    # Action buttons
    def open_add_dialog(e):
        # Clear the fields for new input
        product_name_field.value = ""
        product_category_dropdown.value = None
        product_price_field.value = ""
        product_stock_field.value = ""
        product_barcode_field.value = ""
        product_name_field.error_text = None
        product_category_dropdown.error_text = None
        product_price_field.error_text = None
        product_stock_field.error_text = None

        # Set dialog to add product
        add_product_dialog.title = ft.Text("Add New Product")
        add_product_dialog.actions = [
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(add_product_dialog)),
            ft.TextButton("Add", on_click=add_product),
        ]

        page.dialog = add_product_dialog
        add_product_dialog.open = True
        page.update()

    def open_barcode_scanner(e):
        page.dialog = barcode_scanner_dialog
        barcode_scanner_dialog.open = True
        # Initialize camera when dialog opens
        init_camera()
        page.update()

    export_dialog = ft.AlertDialog(
        title=ft.Text("Export Inventory Data"),
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
        # Create CSV export dialog


        page.dialog = export_dialog
        export_dialog.open = True
        page.update()

    preview_dialog_csv = ft.AlertDialog()
    def export_csv():
        # In a real app, this would save the file to disk
        # For now, we'll simulate successful export

        # Create CSV content as string
        csv_content = "ID,Name,Category,Price,Stock,Barcode\n"
        for product in products:
            csv_content += f"{product['id']},{product['name']},{product['category']},{product['price']},{product['stock']},{product['barcode']}\n"

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
                ft.TextButton("Close", on_click=lambda e: close_dialog(preview_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Close export dialog and show preview
        page.dialog.open = False
        page.dialog = preview_dialog_csv
        preview_dialog_csv.open = True

        # Show success notification
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Inventory data exported successfully to CSV!"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()

    def export_json():
        # Convert products to JSON string
        json_content = json.dumps(products, indent=2)

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
            content=ft.Text("Inventory data exported successfully to JSON!"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()

    action_buttons = ft.Container(
        content=ft.Row([
            ft.ElevatedButton(
                "Add Product",
                icon=ft.icons.ADD,
                on_click=open_add_dialog,
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
            ),
            ft.ElevatedButton(
                "Scan Barcode",
                icon=ft.icons.QR_CODE_SCANNER,
                on_click=open_barcode_scanner,
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

    # Summary cards with properly centered values
    summary_cards = ft.ResponsiveRow([
        ft.Container(
            col={"sm": 6, "md": 3, "lg": 3},
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.INVENTORY_2, color=ft.colors.BLUE_500),
                    ft.Text("Total Products", color=ft.colors.GREY_700, size=subtext_size),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Text(str(len(products)),
                                    size=heading_size,
                                    text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    width=float('inf')  # Make container expand to full width
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
                    ft.Icon(ft.icons.ATTACH_MONEY, color=ft.colors.GREEN_500),
                    ft.Text("Inventory Value", color=ft.colors.GREY_700, size=subtext_size),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Text(f"${sum(p['price'] * p['stock'] for p in products):.2f}",
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
                    ft.Icon(ft.icons.WARNING_AMBER, color=ft.colors.AMBER_500),
                    ft.Text("Low Stock Items", color=ft.colors.GREY_700, size=subtext_size),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Text(str(sum(1 for p in products if p['stock'] < 20)),
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
                    ft.Icon(ft.icons.REMOVE_SHOPPING_CART, color=ft.colors.RED_500),
                    ft.Text("Out of Stock", color=ft.colors.GREY_700, size=subtext_size),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Text(str(sum(1 for p in products if p['stock'] == 0)),
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

    def fetch_price(e):
        if product_name_field.value:
            # Show loading indicator
            product_price_field.label = "Price ($) - Fetching..."
            page.update()

            # In a real app, make an API call here
            # For demo, we'll generate a random price
            import random
            import time
            time.sleep(0.5)  # Simulate API delay
            price = round(random.uniform(1.99, 49.99), 2)

            # Update field with fetched price
            product_price_field.value = str(price)
            product_price_field.label = "Price ($)"
            page.update()

    def add_product(e):
        # Validation for required fields
        if not product_name_field.value:
            product_name_field.error_text = "Name is required"
            page.update()
            return
        if not product_category_dropdown.value:
            product_category_dropdown.error_text = "Category is required"
            page.update()
            return
        if not product_price_field.value:
            product_price_field.error_text = "Price is required"
            page.update()
            return
        if not product_stock_field.value:
            product_stock_field.error_text = "Stock is required"
            page.update()
            return

        try:
            # Parse numeric values
            price = float(product_price_field.value)
            stock = int(product_stock_field.value)

            if price < 0:
                product_price_field.error_text = "Price cannot be negative"
                page.update()
                return

            if stock < 0:
                product_stock_field.error_text = "Stock cannot be negative"
                page.update()
                return

            # Generate a new product ID
            new_id = f"P{(len(products) + 1):03d}"

            # Create new product
            new_product = {
                "id": new_id,
                "name": product_name_field.value,
                "category": product_category_dropdown.value,
                "price": price,
                "stock": stock,
                "barcode": product_barcode_field.value if product_barcode_field.value else "N/A",
            }

            # Add to products list
            products.append(new_product)

            # Update table
            products_table.rows = create_product_rows()

            # Close dialog and show success message
            add_product_dialog.open = False
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Product '{product_name_field.value}' added successfully!"))
            page.snack_bar.open = True
            page.update()

        except ValueError as e:
            # Handle conversion errors
            if 'price' in str(e).lower():
                product_price_field.error_text = "Please enter a valid number"
            else:
                product_stock_field.error_text = "Please enter a valid number"
            page.update()

    def update_product(e):
        # Validation for required fields
        if not product_name_field.value:
            product_name_field.error_text = "Name is required"
            page.update()
            return
        if not product_category_dropdown.value:
            product_category_dropdown.error_text = "Category is required"
            page.update()
            return
        if not product_price_field.value:
            product_price_field.error_text = "Price is required"
            page.update()
            return
        if not product_stock_field.value:
            product_stock_field.error_text = "Stock is required"
            page.update()
            return

        try:
            # Parse numeric values
            price = float(product_price_field.value)
            stock = int(product_stock_field.value)

            if price < 0:
                product_price_field.error_text = "Price cannot be negative"
                page.update()
                return

            if stock < 0:
                product_stock_field.error_text = "Stock cannot be negative"
                page.update()
                return

            # Find and update the product
            for i, product in enumerate(products):
                if product["id"] == edit_product_id:
                    products[i] = {
                        "id": edit_product_id,
                        "name": product_name_field.value,
                        "category": product_category_dropdown.value,
                        "price": price,
                        "stock": stock,
                        "barcode": product_barcode_field.value if product_barcode_field.value else product["barcode"],
                    }
                    break

            # Update table
            products_table.rows = create_product_rows()

            # Close dialog and show success message
            add_product_dialog.open = False
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Product '{product_name_field.value}' updated successfully!"))
            page.snack_bar.open = True
            page.update()

        except ValueError as e:
            # Handle conversion errors
            if 'price' in str(e).lower():
                product_price_field.error_text = "Please enter a valid number"
            else:
                product_stock_field.error_text = "Please enter a valid number"
            page.update()

    add_product_dialog = ft.AlertDialog(
        title=ft.Text("Add New Product"),
        content=ft.Column([
            product_name_field,
            product_category_dropdown,
            ft.Row([
                product_price_field,
                ft.IconButton(
                    icon=ft.icons.REFRESH,
                    tooltip="Fetch price",
                    on_click=fetch_price,
                ),
            ]),
            product_stock_field,
            product_barcode_field,
        ], height=300, width=500, scroll=ft.ScrollMode.AUTO),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(add_product_dialog)),
            ft.TextButton("Add", on_click=add_product),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Real Barcode Scanner Implementation
    camera_view = ft.Image(
        src="/placeholder_camera.png",  # This will be replaced with actual camera feed
        width=320,
        height=240,
        fit=ft.ImageFit.COVER,
        border_radius=10,
    )

    scan_status = ft.Text("Camera initializing...", size=16)
    scanned_barcode = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
    scanned_product_info = ft.Text("", size=14)

    # This would be replaced with actual camera initialization in a real app
    def init_camera():
        scan_status.value = "Camera ready. Position barcode in frame."
        page.update()

        # In a real implementation, you would:
        # 1. Request camera permissions
        # 2. Initialize the camera
        # 3. Set up barcode detection on camera frames

    def process_barcode(barcode_value):
        scanned_barcode.value = f"Barcode: {barcode_value}"

        # Look up product in our database
        product = get_product_by_barcode(barcode_value)

        if product:
            scanned_product_info.value = f"Product found: {product['name']} - ${product['price']:.2f}"
            # Enable the "Add to Inventory" button
            add_scanned_btn.disabled = False
        else:
            scanned_product_info.value = "Product not found. Add as new product."
            # Pre-fill the barcode field in the add product dialog
            product_barcode_field.value = barcode_value
            # Enable the "Add New Product" button
            add_new_product_btn.disabled = False

        page.update()

    # Manual barcode entry for testing
    barcode_input = ft.TextField(
        label="Enter barcode manually (for testing)",
        on_submit=lambda e: process_barcode(e.control.value),
    )

    submit_barcode_btn = ft.ElevatedButton(
        "Process Barcode",
        on_click=lambda e: process_barcode(barcode_input.value) if barcode_input.value else None,
    )

    # Action buttons for the barcode dialog
    add_scanned_btn = ft.ElevatedButton(
        "Add to Inventory",
        icon=ft.icons.ADD_SHOPPING_CART,
        disabled=True,  # Initially disabled until a product is found
        on_click=lambda e: add_scanned_product_to_inventory(),
    )

    add_new_product_btn = ft.ElevatedButton(
        "Add as New Product",
        icon=ft.icons.ADD_CIRCLE,
        disabled=True,  # Initially disabled until a barcode is scanned
        on_click=lambda e: open_add_dialog_with_barcode(),
    )

    # Function to add scanned product to inventory
    def add_scanned_product_to_inventory():
        barcode = scanned_barcode.value.replace("Barcode: ", "")
        product = get_product_by_barcode(barcode)

        if product:
            # Increment stock by 1
            for p in products:
                if p["id"] == product["id"]:
                    p["stock"] += 1
                    break

            # Update table
            products_table.rows = create_product_rows()

            # Show success message
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Added 1 unit of {product['name']} to inventory"))
            page.snack_bar.open = True

            # Close dialog
            close_dialog(barcode_scanner_dialog)
            page.update()

    # Function to open add product dialog with pre-filled barcode
    def open_add_dialog_with_barcode():
        barcode = scanned_barcode.value.replace("Barcode: ", "")
        product_barcode_field.value = barcode

        # Close barcode scanner dialog
        close_dialog(barcode_scanner_dialog)

        # Open add product dialog
        open_add_dialog(None)

    # Create the barcode scanner dialog
    barcode_scanner_dialog = ft.AlertDialog(
        title=ft.Text("Scan Product Barcode"),
        content=ft.Column([
            ft.Container(
                content=camera_view,
                alignment=ft.alignment.center,
                margin=10,
            ),
            scan_status,
            scanned_barcode,
            scanned_product_info,
            ft.Divider(),
            ft.Text("Manual Entry (for testing purposes)", italic=True, size=14),
            barcode_input,
            submit_barcode_btn,
        ], width=400, height=500, scroll=ft.ScrollMode.AUTO),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(barcode_scanner_dialog)),
            add_new_product_btn,
            add_scanned_btn,
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Helper functions
    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def select_product(product_id, selected):
        for row in products_table.rows:
            if row.cells[0].content.value == product_id:
                row.selected = selected
        page.update()

    def edit_product(product_id):
        # Find the product
        global edit_product_id
        edit_product_id = product_id

        # Find the product data
        for product in products:
            if product["id"] == product_id:
                # Fill the form with product data
                product_name_field.value = product["name"]
                product_category_dropdown.value = product["category"]
                product_price_field.value = str(product["price"])
                product_stock_field.value = str(product["stock"])
                product_barcode_field.value = product["barcode"]

                # Clear any error messages
                product_name_field.error_text = None
                product_category_dropdown.error_text = None
                product_price_field.error_text = None
                product_stock_field.error_text = None

                # Set dialog to edit mode
                add_product_dialog.title = ft.Text(f"Edit Product: {product['name']}")
                add_product_dialog.actions = [
                    ft.TextButton("Cancel", on_click=lambda e: close_dialog(add_product_dialog)),
                    ft.TextButton("Update", on_click=update_product),
                ]

                # Show the dialog
                page.dialog = add_product_dialog
                add_product_dialog.open = True
                page.update()
                break

    def delete_product(product_id):
        # Find and remove the product
        for i, product in enumerate(products):
            if product["id"] == product_id:
                # In a real app, you would show a confirmation dialog first
                products.pop(i)
                products_table.rows = create_product_rows()
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Product deleted successfully"))
                page.snack_bar.open = True
                page.update()
                break

    def filter_products(search_text):
        # Filter products based on search text
        if not search_text:
            products_table.rows = create_product_rows()
        else:
            filtered_rows = [
                row for row in create_product_rows()
                if search_text.lower() in row.cells[1].content.value.lower()
            ]
            products_table.rows = filtered_rows
        page.update()

    def filter_by_category(category):
        if category == "All Categories":
            products_table.rows = create_product_rows()
        else:
            filtered_products = [p for p in products if p["category"] == category]
            products_table.rows = [
                row for row in create_product_rows()
                if row.cells[0].content.value in [p["id"] for p in filtered_products]
            ]
        page.update()

    def sort_products(sort_option):
        sorted_products = products.copy()

        if sort_option == "Name (A-Z)":
            sorted_products.sort(key=lambda p: p["name"])
        elif sort_option == "Name (Z-A)":
            sorted_products.sort(key=lambda p: p["name"], reverse=True)
        elif sort_option == "Price (Low-High)":
            sorted_products.sort(key=lambda p: p["price"])
        elif sort_option == "Price (High-Low)":
            sorted_products.sort(key=lambda p: p["price"], reverse=True)
        elif sort_option == "Stock (Low-High)":
            sorted_products.sort(key=lambda p: p["stock"])

        products_table.rows = [
            row for p in sorted_products
            for row in create_product_rows()
            if row.cells[0].content.value == p["id"]
        ]
        page.update()

    # Update UI based on window resize
    def on_resize(e):
        # Update responsive elements based on new width
        is_mobile = page.width <= 800

        # Adjust table scroll mode
        products_table_container.content.controls[0].visible = is_mobile
        products_table_container.content.controls[1].scroll = ft.ScrollMode.ALWAYS if is_mobile else ft.ScrollMode.NONE

        # Adjust button layout
        action_buttons.content.alignment = ft.MainAxisAlignment.CENTER if page.width <= 600 else ft.MainAxisAlignment.START

        page.update()

    page.on_resize = on_resize
    page.drawer = side_drawer

    return ft.View(
        route="/inventory",
        appbar=app_bar,
        controls=[
            side_drawer,
            header,
            summary_cards,
            action_buttons,
            search_row,
            products_table_container,
            add_product_dialog,
            export_dialog
        ],
        scroll=ft.ScrollMode.AUTO
    )