import flet as ft
import random
import time
import json
from datetime import datetime


sample_sales = [
        {"id": "S001", "date": "2023-06-15", "customer": "John Smith", "items": 3, "total": 45.97,
         "status": "Completed", "payment": "Credit Card"},
        {"id": "S002", "date": "2023-06-14", "customer": "Emily Johnson", "items": 1, "total": 12.50,
         "status": "Completed", "payment": "Cash"},
        {"id": "S003", "date": "2023-06-14", "customer": "Michael Brown", "items": 5, "total": 78.25,
         "status": "Completed", "payment": "Credit Card"},
        {"id": "S004", "date": "2023-06-13", "customer": "Sarah Davis", "items": 2, "total": 34.99,
         "status": "Refunded", "payment": "Mobile Payment"},
        {"id": "S005", "date": "2023-06-12", "customer": "Guest Customer", "items": 4, "total": 56.75,
         "status": "Completed", "payment": "Cash"},
    ]

# Initialize sales list at the function level
sales = sample_sales.copy()

    # Sample products for the point of sale
sample_products = [
    {"id": "P001", "name": "Premium Coffee Beans", "category": "Beverages", "price": 14.99, "stock": 45},
    {"id": "P002", "name": "Organic Green Tea", "category": "Beverages", "price": 9.99, "stock": 32},
    {"id": "P003", "name": "Whole Wheat Bread", "category": "Bakery", "price": 4.50, "stock": 18},
    {"id": "P004", "name": "Fresh Apples (1kg)", "category": "Produce", "price": 3.99, "stock": 60},
    {"id": "P005", "name": "Chocolate Cookies", "category": "Snacks", "price": 5.75, "stock": 24},
]


def sales_view(page, app_bar, side_drawer):
    heading_size = 30 if page.width > 800 else 22
    subtext_size = 16 if page.width > 800 else 13
    padding_size = 30 if page.width > 800 else 15

    # Sample data - would be replaced with actual database in production


    # More state variables
    cart_items = []
    customer_name = "Guest Customer"

    # Create data table rows from sales
    def create_sales_rows():
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(sale["id"])),
                    ft.DataCell(ft.Text(sale["date"])),
                    ft.DataCell(ft.Text(sale["customer"])),
                    ft.DataCell(ft.Text(str(sale["items"]))),
                    ft.DataCell(ft.Text(f"${sale['total']:.2f}")),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                sale["status"],
                                color=ft.colors.GREEN if sale["status"] == "Completed" else
                                ft.colors.RED if sale["status"] == "Refunded" else
                                ft.colors.ORANGE,
                            ),
                            padding=5,
                            border_radius=5,
                            bgcolor=ft.colors.GREEN_50 if sale["status"] == "Completed" else
                            ft.colors.RED_50 if sale["status"] == "Refunded" else
                            ft.colors.ORANGE_50,
                        )
                    ),
                    ft.DataCell(ft.Text(sale["payment"])),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.VISIBILITY,
                                icon_color=ft.colors.BLUE,
                                tooltip="View Details",
                                on_click=lambda e, s_id=sale["id"]: view_sale_details(s_id)
                            ),
                            ft.IconButton(
                                icon=ft.icons.RECEIPT_LONG,
                                icon_color=ft.colors.GREEN,
                                tooltip="Print Receipt",
                                on_click=lambda e, s_id=sale["id"]: print_receipt(s_id)
                            ),
                            ft.IconButton(
                                icon=ft.icons.CANCEL,
                                icon_color=ft.colors.RED,
                                tooltip="Refund",
                                on_click=lambda e, s_id=sale["id"]: refund_sale(s_id),
                                disabled=sale["status"] == "Refunded"
                            )
                        ])
                    )
                ]
            ) for sale in sales
        ]

    # Header section
    header = ft.Container(
        padding=padding_size,
        content=ft.Column([
            ft.Text("Sales Management", size=heading_size),
            ft.Text("Process transactions and view sales history", size=subtext_size),
        ])
    )

    # Search and filter section
    search_field = ft.TextField(
        label="Search sales",
        prefix_icon=ft.icons.SEARCH,
        expand=True,
        on_change=lambda e: filter_sales(e.control.value)
    )

    date_range_picker = ft.PopupMenuButton(
        content=ft.Row([
            ft.Icon(ft.icons.DATE_RANGE),
            ft.Text("Date Range", size=subtext_size),
        ]),
        items=[
            ft.PopupMenuItem(text="Today"),
            ft.PopupMenuItem(text="Yesterday"),
            ft.PopupMenuItem(text="Last 7 days"),
            ft.PopupMenuItem(text="This month"),
            ft.PopupMenuItem(text="Last month"),
            ft.PopupMenuItem(text="Custom range..."),
        ],
    )

    status_dropdown = ft.Dropdown(
        label="Status",
        options=[
            ft.dropdown.Option("All"),
            ft.dropdown.Option("Completed"),
            ft.dropdown.Option("Refunded"),
            ft.dropdown.Option("Pending"),
        ],
        value="All",
        width=150,
        on_change=lambda e: filter_by_status(e.control.value)
    )

    payment_dropdown = ft.Dropdown(
        label="Payment Method",
        options=[
            ft.dropdown.Option("All"),
            ft.dropdown.Option("Cash"),
            ft.dropdown.Option("Credit Card"),
            ft.dropdown.Option("Mobile Payment"),
            ft.dropdown.Option("Bank Transfer"),
        ],
        value="All",
        width=180,
        on_change=lambda e: filter_by_payment(e.control.value)
    )

    sort_dropdown = ft.Dropdown(
        label="Sort by",
        options=[
            ft.dropdown.Option("Date (Newest)"),
            ft.dropdown.Option("Date (Oldest)"),
            ft.dropdown.Option("Total (High-Low)"),
            ft.dropdown.Option("Total (Low-High)"),
        ],
        value="Date (Newest)",
        width=180,
        on_change=lambda e: sort_sales(e.control.value)
    )

    search_row = ft.Container(
        content=ft.ResponsiveRow([
            ft.Column([search_field], col={"sm": 12, "md": 6, "lg": 6}),
            ft.Column([
                ft.Row([date_range_picker, status_dropdown, payment_dropdown, sort_dropdown], spacing=10, wrap=True)
            ], col={"sm": 12, "md": 6, "lg": 6},
                horizontal_alignment=ft.CrossAxisAlignment.CENTER if page.width <= 800 else ft.CrossAxisAlignment.END)
        ]),
        padding=ft.padding.only(left=padding_size, right=padding_size, bottom=padding_size)
    )

    # Main sales table
    sales_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Customer")),
            ft.DataColumn(ft.Text("Items")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Payment")),
            ft.DataColumn(ft.Text("Actions")),
        ],
        rows=[],  # Will be populated later
        heading_row_height=70,
        data_row_min_height=60,
        data_row_max_height=80,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
    )

    # Wrap the table in a scrollable container for mobile view
    sales_table_container = ft.Container(
        content=ft.Column([
            # Hint text for mobile users about scrolling
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.SWIPE, color=ft.colors.GREY_500, size=16),
                    ft.Text("Scroll to view more content", color=ft.colors.GREY_500, size=12),
                ], spacing=5),
                visible=page.width <= 800,
                padding=ft.padding.only(bottom=10),
                alignment=ft.alignment.center_right,
            ),
            # Outer container with vertical scrolling
            ft.Column(
                [
                    # Inner row with horizontal scrolling
                    ft.Row(
                        [sales_table],
                        scroll=ft.ScrollMode.ALWAYS if page.width <= 800 else ft.ScrollMode.AUTO,
                        auto_scroll=False,
                    )
                ],
                scroll=ft.ScrollMode.AUTO,  # Vertical scrolling
                height=400,  # Set a fixed height to enable vertical scrolling
                expand=True,  # Allow expansion to fill available space
            )
        ]),
        padding=ft.padding.only(left=padding_size, right=padding_size, bottom=padding_size),
        height=450,  # Set overall container height
    )

    # Helper functions for dialog management
    def close_dialog(dialog):
        dialog.open = False
        page.update()

    # View Sale Details function - FIXED
    sale_details_dialog = ft.AlertDialog(
        open=False,
        title=ft.Text("Sale Details"),
        content=ft.Column([], width=400, height=500, scroll=ft.ScrollMode.AUTO),
        actions=[
            ft.TextButton("Close", on_click=lambda e: close_dialog(sale_details_dialog)),
            ft.ElevatedButton(
                "Print Receipt",
                on_click=lambda e: None,  # Will be updated with the correct function
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def view_sale_details(sale_id):
        # Find the sale
        for sale in sales:
            if sale["id"] == sale_id:
                # Update the existing sale_details_dialog
                sale_details_dialog.title = ft.Text(f"Sale Details - {sale_id}")
                sale_details_dialog.content = ft.Column([
                    ft.Row([
                        ft.Text("Date:", weight=ft.FontWeight.BOLD),
                        ft.Text(sale["date"]),
                    ]),
                    ft.Row([
                        ft.Text("Customer:", weight=ft.FontWeight.BOLD),
                        ft.Text(sale["customer"]),
                    ]),
                    ft.Row([
                        ft.Text("Status:", weight=ft.FontWeight.BOLD),
                        ft.Text(
                            sale["status"],
                            color=ft.colors.GREEN if sale["status"] == "Completed" else
                            ft.colors.RED if sale["status"] == "Refunded" else
                            ft.colors.ORANGE,
                        ),
                    ]),
                    ft.Row([
                        ft.Text("Payment Method:", weight=ft.FontWeight.BOLD),
                        ft.Text(sale["payment"]),
                    ]),
                    ft.Divider(),
                    ft.Text("Items:", weight=ft.FontWeight.BOLD),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Item")),
                            ft.DataColumn(ft.Text("Price")),
                            ft.DataColumn(ft.Text("Qty")),
                            ft.DataColumn(ft.Text("Total")),
                        ],
                        rows=[
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Sample Item 1")),
                                ft.DataCell(ft.Text("$12.99")),
                                ft.DataCell(ft.Text("2")),
                                ft.DataCell(ft.Text("$25.98")),
                            ]),
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Sample Item 2")),
                                ft.DataCell(ft.Text("$9.99")),
                                ft.DataCell(ft.Text("1")),
                                ft.DataCell(ft.Text("$9.99")),
                            ]),
                        ] if not "items_detail" in sale else [
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(item["name"])),
                                ft.DataCell(ft.Text(f"${item['price']:.2f}")),
                                ft.DataCell(ft.Text(str(item["quantity"]))),
                                ft.DataCell(ft.Text(f"${item['price'] * item['quantity']:.2f}")),
                            ]) for item in sale.get("items_detail", [])
                        ],
                    ),
                    ft.Row([
                        ft.Text("Subtotal:", weight=ft.FontWeight.BOLD),
                        ft.Text(f"${sale['total']:.2f}"),
                    ], alignment=ft.MainAxisAlignment.END),
                    ft.Row([
                        ft.Text("Tax:", weight=ft.FontWeight.BOLD),
                        ft.Text(f"${sale['total'] * 0.1:.2f}"),
                    ], alignment=ft.MainAxisAlignment.END),
                    ft.Row([
                        ft.Text("Total:", weight=ft.FontWeight.BOLD, size=18),
                        ft.Text(f"${sale['total'] * 1.1:.2f}", size=18),
                    ], alignment=ft.MainAxisAlignment.END),
                ], width=400, height=500, scroll=ft.ScrollMode.AUTO)

                # Update the print receipt button action
                sale_details_dialog.actions[1].on_click = lambda e: (close_dialog(sale_details_dialog),
                                                                     print_receipt(sale_id))

                # Open the dialog
                sale_details_dialog.open = True
                page.update()
                break

    # Print receipt function
    receipt_dialog = ft.AlertDialog(
        open=False,  # Start with the dialog closed
        title=ft.Text("Receipt"),
        content=ft.Column([], width=400, height=500, scroll=ft.ScrollMode.AUTO),
        actions=[
            ft.TextButton("Close", on_click=lambda e: close_dialog(receipt_dialog)),
            ft.ElevatedButton(
                "Print",
                icon=ft.icons.PRINT,
                on_click=lambda e: simulate_printing(None),  # Will be updated with the correct sale_id
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Then modify the print_receipt function to update this dialog
    def print_receipt(sale_id):
        # Find the sale
        for sale in sales:
            if sale["id"] == sale_id:
                # Update the content of the existing dialog
                receipt_dialog.content = ft.Column([
                    ft.Text("STORE NAME", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text("123 Main Street, City", size=12, text_align=ft.TextAlign.CENTER),
                    ft.Text("Phone: (123) 456-7890", size=12, text_align=ft.TextAlign.CENTER),
                    ft.Divider(thickness=2),
                    ft.Text(f"Receipt #{sale['id']}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Date: {sale['date']} {datetime.now().strftime('%I:%M %p')}"),
                    ft.Text(f"Customer: {sale['customer']}"),
                    ft.Divider(),
                    # ... rest of the content as in your original code ...
                ], width=400, height=500, scroll=ft.ScrollMode.AUTO)

                # Update the print button to use the correct sale_id
                receipt_dialog.actions[1].on_click = lambda e: simulate_printing(sale_id)

                # Open the dialog
                receipt_dialog.open = True
                page.update()
                break

    # Simulate printing
    def simulate_printing(sale_id):
        # In a real app, this would send the receipt to a printer
        # For now, we'll just simulate it with a snackbar
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Printing receipt for sale {sale_id}..."))
        page.snack_bar.open = True
        page.update()

        # Close the receipt dialog
        page.dialog.open = False
        page.update()

    confirm_dialog = ft.AlertDialog(
        open=False,
        title=ft.Text("Confirm Refund"),
        content=ft.Text(""),  # Will be updated with the specific sale ID
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(confirm_dialog)),
            ft.TextButton(
                "Refund",
                on_click=lambda e: None,  # Will be updated with the correct function
                style=ft.ButtonStyle(color=ft.colors.RED),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # ... other dialogs and functions ...

    # Modify the refund_sale function to update the existing dialog
    def refund_sale(sale_id):
        # Update the existing confirm_dialog
        confirm_dialog.title = ft.Text("Confirm Refund")
        confirm_dialog.content = ft.Text(
            f"Are you sure you want to refund sale {sale_id}? This action cannot be undone.")

        # Update the refund button action
        confirm_dialog.actions[1].on_click = lambda e: process_refund(sale_id)

        # Open the dialog
        confirm_dialog.open = True
        page.update()

    # Process refund
    def process_refund(sale_id):
        # Find and update the sale status
        for i, sale in enumerate(sales):
            if sale["id"] == sale_id:
                sales[i]["status"] = "Refunded"

                # Update table
                sales_table.rows = create_sales_rows()

                # Close dialog and show success message
                page.dialog.open = False
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Sale {sale_id} has been refunded"))
                page.snack_bar.open = True
                page.update()
                break

    # Cart display for POS
    cart_display = ft.ListView(
        height=300,
        spacing=10,
        padding=10,
        auto_scroll=True,
    )

    # Cart summary display
    cart_total_text = ft.Text("Total: $0.00", size=20, weight=ft.FontWeight.BOLD)
    cart_items_text = ft.Text("Items: 0")

    def update_cart_display():
        cart_display.controls.clear()
        for item in cart_items:
            cart_display.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(item["name"], expand=True),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.REMOVE,
                                on_click=lambda e, i=item: decrease_quantity(i),
                                icon_size=16,
                            ),
                            ft.Text(f"{item['quantity']}"),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                on_click=lambda e, i=item: increase_quantity(i),
                                icon_size=16,
                            ),
                        ], spacing=0),
                        ft.Text(f"${item['price'] * item['quantity']:.2f}", width=80, text_align=ft.TextAlign.RIGHT),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=lambda e, i=item: remove_from_cart(i),
                            icon_color=ft.colors.RED,
                            icon_size=16,
                        ),
                    ]),
                    border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.GREY_300)),
                    padding=5,
                )
            )

        cart_total_text.value = f"Total: ${sum(item['price'] * item['quantity'] for item in cart_items):.2f}"
        cart_items_text.value = f"Items: {sum(item['quantity'] for item in cart_items)}"

        page.update()

    def add_to_cart(product):
        # Check if the product is already in the cart
        for item in cart_items:
            if item["id"] == product["id"]:
                item["quantity"] += 1
                update_cart_display()
                return

        # Add new product to cart
        cart_items.append({
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": 1
        })
        update_cart_display()

    def increase_quantity(item):
        item["quantity"] += 1
        update_cart_display()

    def decrease_quantity(item):
        if item["quantity"] > 1:
            item["quantity"] -= 1
            update_cart_display()

    def remove_from_cart(item):
        cart_items.remove(item)
        update_cart_display()

    def clear_cart():
        cart_items.clear()
        update_cart_display()

    # Customer information
    customer_name_field = ft.TextField(
        label="Customer Name",
        value="Guest Customer",
        on_change=lambda e: set_customer_name(e.control.value),
    )

    def set_customer_name(name):
        nonlocal customer_name
        customer_name = name if name else "Guest Customer"

    # Payment method selection
    payment_method = ft.Dropdown(
        label="Payment Method",
        options=[
            ft.dropdown.Option("Cash"),
            ft.dropdown.Option("Credit Card"),
            ft.dropdown.Option("Mobile Payment"),
            ft.dropdown.Option("Bank Transfer"),
        ],
        value="Cash",
        width=200,
    )

    # Product grid for POS
    def create_product_cards():
        product_grid = ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=0.8,
            spacing=10,
            run_spacing=10,
        )

        for product in sample_products:
            product_grid.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(product["name"], size=14, weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER),
                            ft.Text(f"${product['price']:.2f}", size=16, text_align=ft.TextAlign.CENTER),
                            ft.Text(f"Stock: {product['stock']}", size=12, text_align=ft.TextAlign.CENTER,
                                    color=ft.colors.GREY_700),
                            ft.ElevatedButton(
                                "Add to Cart",
                                on_click=lambda e, p=product: add_to_cart(p),
                                width=120,
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=10,
                        width=140,
                        height=160,
                    ),
                    elevation=2,
                )
            )
        return product_grid

    product_cards = create_product_cards()

    # Action buttons
    def open_new_sale_dialog(e):
        # Reset cart for new sale
        cart_items.clear()
        update_cart_display()

        # Open the POS dialog
        page.dialog = pos_dialog
        pos_dialog.open = True
        customer_name_field.value = "Guest Customer"
        page.update()

    def open_reports_dialog(e):
        # Generate reports
        show_reports()

    def open_export_dialog():
        # Create CSV export dialog
        export_dialog = ft.AlertDialog(
            title=ft.Text("Export Sales Data"),
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
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.icons.FILE_PRESENT),
                            ft.Text("PDF"),
                        ]),
                        on_click=lambda e: export_pdf(),
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ], width=400, tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog(export_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = export_dialog
        export_dialog.open = True
        page.update()

    action_buttons = ft.Container(
        content=ft.Row([
            ft.ElevatedButton(
                "New Sale",
                icon=ft.icons.SHOPPING_CART_CHECKOUT,
                on_click=open_new_sale_dialog,
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
            ),
            ft.ElevatedButton(
                "Reports",
                icon=ft.icons.ASSESSMENT,
                on_click=open_reports_dialog,
                bgcolor=ft.colors.GREEN,
                color=ft.colors.WHITE,
            ),
            ft.ElevatedButton(
                "Export Data",
                icon=ft.icons.DOWNLOAD,
                on_click=lambda e: open_export_dialog(),
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
                    ft.Icon(ft.icons.RECEIPT, color=ft.colors.BLUE_500),
                    ft.Text("Total Sales", color=ft.colors.GREY_700, size=subtext_size),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Text(str(len(sales)),
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
                    ft.Text("Revenue", color=ft.colors.GREY_700, size=subtext_size),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Text(f"${sum(s['total'] for s in sales if s['status'] != 'Refunded'):.2f}",
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
                    ft.Icon(ft.icons.TODAY, color=ft.colors.AMBER_500),
                    ft.Text("Today's Sales", color=ft.colors.GREY_700, size=subtext_size),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Text(str(sum(1 for s in sales if s['date'] == datetime.now().strftime('%Y-%m-%d'))),
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
                    ft.Icon(ft.icons.ASSIGNMENT_RETURN, color=ft.colors.RED_500),
                    ft.Text("Refunds", color=ft.colors.GREY_700, size=subtext_size),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Text(str(sum(1 for s in sales if s['status'] == 'Refunded')),
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

    # Checkout function
    def checkout(e):
        if not cart_items:
            # Show error if cart is empty
            page.snack_bar = ft.SnackBar(content=ft.Text("Cart is empty. Add items before checkout."))
            page.snack_bar.open = True
            page.update()
            return

        # Calculate totals
        total_amount = sum(item["price"] * item["quantity"] for item in cart_items)
        total_items = sum(item["quantity"] for item in cart_items)

        # Create a new sale
        new_sale = {
            "id": f"S{(len(sales) + 1):03d}",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "customer": customer_name,
            "items": total_items,
            "total": total_amount,
            "status": "Completed",
            "payment": payment_method.value,
            "items_detail": cart_items.copy()  # Save detailed cart info
        }

        # Add to sales list
        sales.append(new_sale)

        # Update sales table
        sales_table.rows = create_sales_rows()

        # Show receipt
        show_receipt(new_sale)

        # Close POS dialog
        pos_dialog.open = False
        page.update()

        # Show success message
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Sale completed successfully! Total: ${total_amount:.2f}"))
        page.snack_bar.open = True
        page.update()

    # Create the POS dialog
    pos_dialog = ft.AlertDialog(
        title=ft.Text("Point of Sale"),
        content=ft.Container(
            content=ft.ListView(
                [
                    ft.Container(
                        content=ft.Tabs(
                            selected_index=0,
                            animation_duration=300,
                            tabs=[
                                ft.Tab(
                                    text="Products",
                                    content=ft.Container(
                                        content=product_cards,
                                        padding=10,
                                    ),
                                ),
                                ft.Tab(
                                    text="Categories",
                                    content=ft.Container(
                                        content=ft.Column([
                                            ft.Text("Product categories will be shown here")
                                        ]),
                                        padding=10,
                                    ),
                                ),
                                ft.Tab(
                                    text="Search",
                                    content=ft.Container(
                                        content=ft.Column([
                                            ft.TextField(label="Search products", prefix_icon=ft.icons.SEARCH),
                                            ft.Container(height=10),
                                            ft.Text("Search results will appear here")
                                        ]),
                                        padding=10,
                                    ),
                                ),
                            ],
                        ),
                        height=300,
                        border=ft.border.all(1, ft.colors.GREY_300),
                        border_radius=5,
                    ),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("Shopping Cart", size=16, weight=ft.FontWeight.BOLD),
                                ft.TextButton("Clear Cart", on_click=lambda e: clear_cart()),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Container(
                                content=cart_display,
                                border=ft.border.all(1, ft.colors.GREY_300),
                                border_radius=5,
                                padding=5,
                                height=200,
                            ),
                            ft.Row([
                                cart_items_text,
                                cart_total_text,
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(),
                            customer_name_field,
                            payment_method,
                        ]),
                        padding=10,
                    ),
                ],
                auto_scroll=True,  # Enable auto-scrolling
                spacing=0,
            ),
            width=800,
            height=700,
        ),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(pos_dialog)),
            ft.ElevatedButton(
                "Checkout",
                bgcolor=ft.colors.GREEN,
                color=ft.colors.WHITE,
                on_click=checkout
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Show receipt for new sale
    def show_receipt(sale):
        receipt_dialog = ft.AlertDialog(
            title=ft.Text("Receipt"),
            content=ft.Column([
                ft.Text("STORE NAME", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text("123 Main Street, City", size=12, text_align=ft.TextAlign.CENTER),
                ft.Text("Phone: (123) 456-7890", size=12, text_align=ft.TextAlign.CENTER),
                ft.Divider(thickness=2),
                ft.Text(f"Receipt #{sale['id']}", weight=ft.FontWeight.BOLD),
                ft.Text(f"Date: {sale['date']} {datetime.now().strftime('%I:%M %p')}"),
                ft.Text(f"Customer: {sale['customer']}"),
                ft.Divider(),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Item")),
                        ft.DataColumn(ft.Text("Qty")),
                        ft.DataColumn(ft.Text("Price")),
                        ft.DataColumn(ft.Text("Total")),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(item["name"])),
                            ft.DataCell(ft.Text(str(item["quantity"]))),
                            ft.DataCell(ft.Text(f"${item['price']:.2f}")),
                            ft.DataCell(ft.Text(f"${item['price'] * item['quantity']:.2f}")),
                        ]) for item in sale.get("items_detail", cart_items)
                    ],
                ),
                ft.Divider(),
                ft.Row([
                    ft.Text("Subtotal:", weight=ft.FontWeight.BOLD),
                    ft.Text(f"${sale['total']:.2f}"),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("Tax (10%):", weight=ft.FontWeight.BOLD),
                    ft.Text(f"${sale['total'] * 0.1:.2f}"),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(thickness=2),
                ft.Row([
                    ft.Text("TOTAL:", weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(f"${sale['total'] * 1.1:.2f}", size=16, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=20),
                ft.Text(f"Payment Method: {sale['payment']}", size=14),
                ft.Container(height=10),
                ft.Text("Thank you for your purchase!", size=14, italic=True, text_align=ft.TextAlign.CENTER),
            ], width=400, height=500, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Close", on_click=lambda e: close_dialog(receipt_dialog)),
                ft.ElevatedButton(
                    "Print",
                    icon=ft.icons.PRINT,
                    on_click=lambda e: simulate_printing(sale['id']),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = receipt_dialog
        receipt_dialog.open = True
        page.update()

        # Clear cart after showing receipt
        cart_items.clear()

    # Create weekly chart
    def create_weekly_chart():
        # Sample data for the chart
        weekly_data = [
            ("Mon", 120),
            ("Tue", 90),
            ("Wed", 160),
            ("Thu", 80),
            ("Fri", 140),
            ("Sat", 200),
            ("Sun", 160),
        ]

        bar_groups = []
        bottom_labels = []

        for idx, (day, revenue) in enumerate(weekly_data):
            bar_groups.append(
                ft.BarChartGroup(
                    x=idx,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=revenue,
                            width=30,
                            color=ft.colors.BLUE_500,
                            tooltip=f"{day}: ${revenue}",
                            border_radius=0,
                        )
                    ]
                )
            )

            bottom_labels.append(
                ft.ChartAxisLabel(
                    value=idx,
                    label=ft.Container(ft.Text(day), padding=5),
                )
            )

        chart = ft.BarChart(
            bar_groups=bar_groups,
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels_size=30,
                title_size=20,
            ),
            bottom_axis=ft.ChartAxis(
                labels=bottom_labels,
                labels_size=40,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.9, ft.colors.BLUE_200),
            max_y=max([r for _, r in weekly_data]) + 20,
            interactive=True,
            expand=True,
        )

        return chart

    # Show reports dialog
    today = datetime.now().strftime('%Y-%m-%d')
    daily_sales = sum(1 for s in sales if s['date'] == today)
    daily_revenue = sum(s['total'] for s in sales if s['date'] == today and s['status'] != 'Refunded')

    # Payment method breakdown
    payment_methods = {}
    for sale in sales:
        if sale['payment'] not in payment_methods:
            payment_methods[sale['payment']] = 0
        payment_methods[sale['payment']] += 1

    # Create report dialog
    global report_dialog
    report_dialog = ft.AlertDialog(
        title=ft.Text("Sales Reports"),
        content=ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Daily Summary",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"Date: {today}", size=16, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=ft.Row([
                                    ft.Column([
                                        ft.Text("Total Sales", size=14, color=ft.colors.GREY_700),
                                        ft.Text(f"{daily_sales}", size=24, weight=ft.FontWeight.BOLD),
                                    ], alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    ft.VerticalDivider(width=1, thickness=1),
                                    ft.Column([
                                        ft.Text("Revenue", size=14, color=ft.colors.GREY_700),
                                        ft.Text(f"${daily_revenue:.2f}", size=24, weight=ft.FontWeight.BOLD),
                                    ], alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                                padding=20,
                                border=ft.border.all(1, ft.colors.GREY_400),
                                border_radius=10,
                                margin=ft.margin.only(top=10, bottom=20),
                            ),
                            ft.Text("Payment Methods Breakdown", size=16, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text(payment, expand=True),
                                        ft.Text(f"{count} ({count / len(sales) * 100:.1f}%)"),
                                    ]) for payment, count in payment_methods.items()
                                ]),
                                border=ft.border.all(1, ft.colors.GREY_400),
                                border_radius=10,
                                padding=20,
                            ),
                        ]),
                        padding=20,
                        height=450,  # Increased height
                    ),
                ),
                ft.Tab(
                    text="Weekly Chart",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Weekly Sales Overview", size=16, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=create_weekly_chart(),
                                height=400,  # Increased height for chart
                                margin=10,
                            ),
                        ]),
                        padding=20,
                        height=500,  # Increased container height
                    ),
                ),
                ft.Tab(
                    text="Product Analysis",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Top Selling Products", size=16, weight=ft.FontWeight.BOLD),
                            # Wrap table in a scrollable container
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.DataTable(
                                            columns=[
                                                ft.DataColumn(ft.Text("Product")),
                                                ft.DataColumn(ft.Text("Quantity")),
                                                ft.DataColumn(ft.Text("Revenue")),
                                            ],
                                            rows=[
                                                ft.DataRow(cells=[
                                                    ft.DataCell(ft.Text("Premium Coffee Beans")),
                                                    ft.DataCell(ft.Text("12")),
                                                    ft.DataCell(ft.Text("$179.88")),
                                                ]),
                                                ft.DataRow(cells=[
                                                    ft.DataCell(ft.Text("Organic Green Tea")),
                                                    ft.DataCell(ft.Text("8")),
                                                    ft.DataCell(ft.Text("$79.92")),
                                                ]),
                                                ft.DataRow(cells=[
                                                    ft.DataCell(ft.Text("Whole Wheat Bread")),
                                                    ft.DataCell(ft.Text("5")),
                                                    ft.DataCell(ft.Text("$22.50")),
                                                ]),
                                            ],
                                            # Improved table styling
                                            heading_row_height=60,
                                            data_row_min_height=50,
                                            data_row_max_height=60,
                                            column_spacing=20,
                                            border=ft.border.all(1, ft.colors.GREY_400),
                                            border_radius=8,
                                        ),
                                    ],
                                    scroll=ft.ScrollMode.AUTO,  # Add horizontal scrolling if needed
                                ),
                                margin=ft.margin.only(top=10),
                                padding=15,
                                height=300,
                                border=ft.border.all(1, ft.colors.GREY_200),
                                border_radius=10,
                            ),
                        ]),
                        padding=20,
                        height=450,  # Increased container height
                    ),
                ),
            ],
            width=650,  # Increased overall width
            height=550,  # Increased overall height
        ),
        actions=[
            ft.TextButton("Close", on_click=lambda e: close_dialog(report_dialog)),
            ft.ElevatedButton(
                "Export Report",
                icon=ft.icons.DOWNLOAD,
                on_click=lambda e: export_report(),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    def show_reports():
        # Calculate report data

        page.controls.append(report_dialog)
        page.dialog = report_dialog
        report_dialog.open = True
        page.update()

    # Export report
    def export_report():
        # Simulate report export
        page.snack_bar = ft.SnackBar(content=ft.Text("Exporting sales report..."))
        page.snack_bar.open = True
        page.update()

        # Close dialog
        page.dialog.open = False
        page.update()

    def export_csv():
        # In a real app, this would save the file to disk
        # For now, we'll simulate successful export

        # Create CSV content as string
        csv_content = "ID,Date,Customer,Items,Total,Status,Payment\n"
        for sale in sales:
            csv_content += f"{sale['id']},{sale['date']},{sale['customer']},{sale['items']},{sale['total']},{sale['status']},{sale['payment']}\n"

        # Show confirmation with preview
        preview_dialog = ft.AlertDialog(
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
        page.dialog = preview_dialog
        preview_dialog.open = True

        # Show success notification
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Sales data exported successfully to CSV!"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()

    def export_json():
        # Convert products to JSON string
        json_content = json.dumps(sales, indent=2)

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
            content=ft.Text("Sales data exported successfully to JSON!"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()

    def export_pdf():
        # In a real app, this would generate a PDF
        # For now, we'll simulate it

        # Show generating message
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Generating PDF report..."),
        )
        page.snack_bar.open = True
        page.update()

        # Close dialog
        page.dialog.open = False

        # After a brief delay, show success
        time.sleep(1)

        page.snack_bar = ft.SnackBar(
            content=ft.Text("Sales data exported successfully to PDF!"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()

    def filter_sales(search_text):
        # Filter sales based on search text
        if not search_text:
            sales_table.rows = create_sales_rows()
        else:
            filtered_rows = [
                row for row in create_sales_rows()
                if search_text.lower() in row.cells[0].content.value.lower() or  # ID
                   search_text.lower() in row.cells[2].content.value.lower()  # Customer
            ]
            sales_table.rows = filtered_rows
        page.update()

    def filter_by_status(status):
        if status == "All":
            sales_table.rows = create_sales_rows()
        else:
            filtered_sales = [s for s in sales if s["status"] == status]
            filtered_rows = [
                row for row in create_sales_rows()
                if row.cells[0].content.value in [s["id"] for s in filtered_sales]
            ]
            sales_table.rows = filtered_rows
        page.update()

    def filter_by_payment(payment):
        if payment == "All":
            sales_table.rows = create_sales_rows()
        else:
            filtered_sales = [s for s in sales if s["payment"] == payment]
            filtered_rows = [
                row for row in create_sales_rows()
                if row.cells[0].content.value in [s["id"] for s in filtered_sales]
            ]
            sales_table.rows = filtered_rows
        page.update()

    def sort_sales(sort_option):
        global sales
        sorted_sales = sales

        if sort_option == "Date (Newest)":
            sorted_sales.sort(key=lambda s: s["date"], reverse=True)
        elif sort_option == "Date (Oldest)":
            sorted_sales.sort(key=lambda s: s["date"])
        elif sort_option == "Total (High-Low)":
            sorted_sales.sort(key=lambda s: s["total"], reverse=True)
        elif sort_option == "Total (Low-High)":
            sorted_sales.sort(key=lambda s: s["total"])

        sales = sorted_sales  # this is fine now

        # Refresh the table
        sales_table.rows = create_sales_rows()
        page.update()

    # Update UI based on window resize
    def on_resize(e):
        # Update responsive elements based on new width
        is_mobile = page.width <= 800

        # Adjust table scroll mode
        sales_table_container.content.controls[0].visible = is_mobile
        sales_table_container.content.controls[1].scroll = ft.ScrollMode.ALWAYS if is_mobile else ft.ScrollMode.AUTO

        # Adjust button layout
        action_buttons.content.alignment = ft.MainAxisAlignment.CENTER if page.width <= 600 else ft.MainAxisAlignment.START

        page.update()

    # Initialize table rows
    sales_table.rows = create_sales_rows()

    # Set event handlers
    page.on_resize = on_resize
    page.drawer = side_drawer

    return ft.View(
        route="/sales",
        appbar=app_bar,
        controls=[
            side_drawer,
            header,
            summary_cards,
            action_buttons,
            search_row,
            sales_table_container,
            pos_dialog,
            report_dialog,
            receipt_dialog,
            sale_details_dialog,
            confirm_dialog
        ],
        scroll=ft.ScrollMode.AUTO
    )