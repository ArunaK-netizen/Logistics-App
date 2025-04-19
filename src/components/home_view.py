import flet as ft
from datetime import datetime


def home_view(page, app_bar, side_drawer):
    heading_size = 30 if page.width > 800 else 22
    subtext_size = 16 if page.width > 800 else 13
    padding_size = 30 if page.width > 800 else 15

    # Color constants for consistency
    primary_color = ft.colors.BLUE_500
    accent_color = ft.colors.GREEN_500
    border_color = ft.colors.GREY_400

    # In home_view.py, update your metrics display

    # Update recent activity
    recent_activity_list = []
    for activity in page.app_state['recent_activities'][:3]:  # Show 3 most recent
        recent_activity_list.append(
            ft.ListTile(
                leading=ft.Icon(
                    ft.icons.SHOPPING_BAG if activity['type'] == 'sale' else ft.icons.INVENTORY,
                    color=primary_color
                ),
                title=ft.Text(activity['title']),
                subtitle=ft.Text(activity['subtitle']),
                trailing=ft.Text(activity['time'], size=subtext_size - 3, color=ft.colors.GREY_500),
            )
        )


    # Define all dialogs at the beginning
    product_details_dialog = ft.AlertDialog(
        open=False,
        title=ft.Text("Product Details"),
        content=ft.Column([], width=400, height=300, scroll=ft.ScrollMode.AUTO),
        actions=[
            ft.TextButton("Close", on_click=lambda e: close_dialog(product_details_dialog)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    low_stock_dialog = ft.AlertDialog(
        open=False,
        title=ft.Text("Low Stock Items"),
        content=ft.Column([], width=400, height=300, scroll=ft.ScrollMode.AUTO),
        actions=[
            ft.TextButton("Close", on_click=lambda e: close_dialog(low_stock_dialog)),
            ft.ElevatedButton(
                "Order More",
                icon=ft.icons.ADD_SHOPPING_CART,
                on_click=lambda e: (close_dialog(low_stock_dialog), open_order_items())
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    order_dialog = ft.AlertDialog(
        open=False,
        title=ft.Text("Order Inventory"),
        content=ft.Column([], width=400, height=400, scroll=ft.ScrollMode.AUTO),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(order_dialog)),
            ft.ElevatedButton("Place Order", on_click=lambda e: place_order()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    revenue_details_dialog = ft.AlertDialog(
        open=False,
        title=ft.Text("Revenue Details"),
        content=ft.Column([], width=500, height=400, scroll=ft.ScrollMode.AUTO),
        actions=[
            ft.TextButton("Close", on_click=lambda e: close_dialog(revenue_details_dialog)),
            ft.ElevatedButton(
                "Export Report",
                icon=ft.icons.DOWNLOAD,
                on_click=lambda e: export_report()
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Helper functions for dialogs
    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def show_product_details(product_id=None):
        # Sample product data
        products = [
            {"id": 1, "name": "Product A", "price": 19.99, "stock": 12, "description": "High-quality product A"},
            {"id": 2, "name": "Product B", "price": 29.99, "stock": 8, "description": "Premium product B"},
            {"id": 3, "name": "Product C", "price": 9.99, "stock": 2, "description": "Budget-friendly product C"}
        ]

        # Find product or show all if no ID specified
        if product_id:
            product = next((p for p in products if p["id"] == product_id), None)
            if product:
                product_details_dialog.title = ft.Text(f"Product Details - {product['name']}")
                product_details_dialog.content = ft.Column([
                    ft.Row([
                        ft.Text("Product ID:", weight=ft.FontWeight.BOLD),
                        ft.Text(str(product["id"]))
                    ]),
                    ft.Row([
                        ft.Text("Name:", weight=ft.FontWeight.BOLD),
                        ft.Text(product["name"])
                    ]),
                    ft.Row([
                        ft.Text("Price:", weight=ft.FontWeight.BOLD),
                        ft.Text(f"${product['price']}")
                    ]),
                    ft.Row([
                        ft.Text("In Stock:", weight=ft.FontWeight.BOLD),
                        ft.Text(
                            str(product["stock"]),
                            color=ft.colors.RED if product["stock"] < 5 else ft.colors.GREEN
                        )
                    ]),
                    ft.Divider(),
                    ft.Text("Description:", weight=ft.FontWeight.BOLD),
                    ft.Text(product["description"]),
                ], width=400, scroll=ft.ScrollMode.AUTO)
            else:
                product_details_dialog.title = ft.Text("Product Not Found")
                product_details_dialog.content = ft.Text("The specified product could not be found.")
        else:
            # Show all products
            rows = []
            for product in products:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(product["name"])),
                            ft.DataCell(ft.Text(f"${product['price']}")),
                            ft.DataCell(ft.Text(
                                str(product["stock"]),
                                color=ft.colors.RED if product["stock"] < 5 else ft.colors.GREEN
                            )),
                        ]
                    )
                )

            product_details_dialog.title = ft.Text("All Products")
            product_details_dialog.content = ft.Column([
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Product")),
                        ft.DataColumn(ft.Text("Price")),
                        ft.DataColumn(ft.Text("Stock")),
                    ],
                    rows=rows,
                )
            ], width=400, scroll=ft.ScrollMode.AUTO)

        product_details_dialog.open = True
        page.update()

    def show_low_stock_items():
        # Sample low stock data
        low_stock_items = [
            {"id": 3, "name": "Product C", "stock": 2, "min_stock": 5},
        ]

        rows = []
        for item in low_stock_items:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["name"])),
                        ft.DataCell(ft.Text(str(item["stock"]))),
                        ft.DataCell(ft.Text(str(item["min_stock"]))),
                    ]
                )
            )

        low_stock_dialog.content = ft.Column([
            ft.Text("The following items are below their minimum stock level:", size=subtext_size),
            ft.Container(height=10),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Product")),
                    ft.DataColumn(ft.Text("Current Stock")),
                    ft.DataColumn(ft.Text("Min. Stock")),
                ],
                rows=rows,
            )
        ], width=400, scroll=ft.ScrollMode.AUTO)

        low_stock_dialog.open = True
        page.update()

    def open_order_items():
        # Sample order form
        order_dialog.content = ft.Column([
            ft.Text("Order new inventory items", size=subtext_size),
            ft.Container(height=10),
            ft.Dropdown(
                label="Supplier",
                hint_text="Select a supplier",
                options=[
                    ft.dropdown.Option("Supplier A"),
                    ft.dropdown.Option("Supplier B"),
                    ft.dropdown.Option("Supplier C"),
                ]
            ),
            ft.Container(height=10),
            ft.Text("Items to order:"),
            ft.Checkbox(label="Product C (Low Stock)", value=True),
            ft.TextField(label="Quantity", value="10"),
            ft.Checkbox(label="Product B"),
            ft.TextField(label="Quantity", value="5"),
            ft.Checkbox(label="Product A"),
            ft.TextField(label="Quantity", value="0"),
            ft.Container(height=10),
            ft.TextField(label="Additional Notes", multiline=True),
        ], width=400, scroll=ft.ScrollMode.AUTO)

        order_dialog.open = True
        page.update()

    def place_order():
        # In a real app, this would process the order
        order_dialog.open = False
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Order placed successfully!"),
            action="Dismiss",
        )
        page.snack_bar.open = True
        page.update()

    def show_revenue_details(date=None):
        # Sample revenue data
        revenue_details_dialog.title = ft.Text("Revenue Details" + (f" - {date}" if date else ""))

        # Create sample data for the detailed view
        transaction_rows = []
        for i in range(1, 6):
            transaction_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"TR-{1000 + i}")),
                        ft.DataCell(ft.Text(f"Customer {i}")),
                        ft.DataCell(ft.Text(f"${30 + i * 10}.99")),
                        ft.DataCell(ft.Text("Completed")),
                    ]
                )
            )

        revenue_details_dialog.content = ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Text("Period:", weight=ft.FontWeight.BOLD),
                    ft.Text(date or "This Week"),
                ]),
                padding=10
            ),
            ft.Container(
                content=ft.Row([
                    ft.Text("Total Revenue:", weight=ft.FontWeight.BOLD),
                    ft.Text(f"${page.app_state['total_sales']:.2f}", size=heading_size - 4),
                ]),
                padding=10
            ),
            ft.Divider(),
            ft.Text("Transactions:", weight=ft.FontWeight.BOLD),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Customer")),
                    ft.DataColumn(ft.Text("Amount")),
                    ft.DataColumn(ft.Text("Status")),
                ],
                rows=transaction_rows,
            ),
            ft.Container(height=10),
            ft.Text("Revenue Breakdown:", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text("By Product", weight=ft.FontWeight.BOLD, size=subtext_size),
                        ft.Text("Product A: $110.99"),
                        ft.Text("Product B: $89.97"),
                        ft.Text("Product C: $49.00"),
                    ]),
                    expand=1,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("By Payment Method", weight=ft.FontWeight.BOLD, size=subtext_size),
                        ft.Text("Credit Card: $190.96"),
                        ft.Text("Cash: $39.00"),
                        ft.Text("Other: $20.00"),
                    ]),
                    expand=1,
                )
            ]),
        ], width=500, height=400, scroll=ft.ScrollMode.AUTO)

        revenue_details_dialog.open = True
        page.update()

    def export_report():
        # In a real app, this would generate a report
        revenue_details_dialog.open = False
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Report exported successfully!"),
            action="Dismiss",
        )
        page.snack_bar.open = True
        page.update()

    # Header section
    header = ft.Container(
        padding=padding_size,
        content=ft.Column([
            ft.Text("Dashboard", size=heading_size, weight=ft.FontWeight.BOLD),
            ft.Text("Welcome back, here's your store overview", size=subtext_size),
        ], spacing=5)
    )

    # Quick action cards with click functionality
    cards = ft.ResponsiveRow([
        ft.Container(
            col={"sm": 4, "md": 4, "lg": 4},
            padding=padding_size,
            border=ft.border.all(1, border_color),
            border_radius=10,
            ink=True,  # Enable ripple effect
            content=ft.Column(
                [
                    ft.Icon(ft.icons.INVENTORY_2_OUTLINED, size=30, color=primary_color),
                    ft.Text("Manage Products", size=subtext_size),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            on_click=lambda _: show_product_details()  # Show products dialog when clicked
        ),
        ft.Container(
            col={"sm": 4, "md": 4, "lg": 4},
            padding=padding_size,
            border=ft.border.all(1, border_color),
            border_radius=10,
            ink=True,
            content=ft.Column(
                [
                    ft.Icon(ft.icons.PEOPLE_OUTLINE, size=30, color=ft.colors.INDIGO_400),
                    ft.Text("View Customers", size=subtext_size),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            on_click=lambda _: page.go("/customers")  # Navigate to customers page
        ),
        ft.Container(
            col={"sm": 4, "md": 4, "lg": 4},
            padding=padding_size,
            border=ft.border.all(1, border_color),
            border_radius=10,
            ink=True,
            content=ft.Column(
                [
                    ft.Icon(ft.icons.SHOPPING_CART_OUTLINED, size=30, color=accent_color),
                    ft.Text("Process Sales", size=subtext_size),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            on_click=lambda _: page.go("/sales")  # Navigate to sales page
        )
    ])

    # Summary metrics section
    insights_item_width = page.width // 2
    insights = ft.GridView(
        expand=1,
        max_extent=insights_item_width,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )

    insights.controls.append(
        ft.Container(
            padding=padding_size,
            border=ft.border.all(1, border_color),
            border_radius=10,
            ink=True,  # Enable ripple effect
            on_click=lambda _: show_revenue_details(),  # Show revenue details when clicked
            content=ft.Column(
                [
                    ft.Row(
                        spacing=5,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Total Sales", size=subtext_size, color=ft.colors.GREY_700),
                            ft.Icon(ft.icons.ATTACH_MONEY, size=subtext_size + 2, color=ft.colors.GREEN_900),
                        ]
                    ),
                    ft.Text("$249.96", size=heading_size, weight=ft.FontWeight.BOLD),
                    ft.Text("↑ 12.5%", size=subtext_size, color=ft.colors.GREEN_500)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            )
        )
    )

    insights.controls.append(
        ft.Container(
            padding=padding_size,
            border=ft.border.all(1, border_color),
            border_radius=10,
            ink=True,
            on_click=lambda _: page.go("/sales"),  # Navigate to sales page when clicked
            content=ft.Column(
                [
                    ft.Row(
                        spacing=5,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Total Orders", size=subtext_size, color=ft.colors.GREY_700),
                            ft.Icon(ft.icons.SHOPPING_CART_CHECKOUT, size=subtext_size + 2,
                                    color=ft.colors.BLUE_GREY_500),
                        ]
                    ),
                    ft.Text(str(page.app_state['total_orders']), size=heading_size, weight=ft.FontWeight.BOLD),
                    ft.Text("↑ 8.2%", size=subtext_size, color=ft.colors.GREEN_500)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            )
        )
    )

    insights.controls.append(
        ft.Container(
            padding=padding_size,
            border=ft.border.all(1, border_color),
            border_radius=10,
            ink=True,
            on_click=lambda _: page.go("/inventory"),  # Navigate to inventory page when clicked
            content=ft.Column(
                [
                    ft.Row(
                        spacing=5,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Prod. in Stock", size=subtext_size, color=ft.colors.GREY_700),
                            ft.Icon(ft.icons.INVENTORY, size=subtext_size + 2, color=ft.colors.AMBER_500),
                        ]
                    ),
                    ft.Text(str(page.app_state['products_in_stock']), size=heading_size, weight=ft.FontWeight.BOLD),
                    ft.Text("↓ 3.1%", size=subtext_size, color=ft.colors.RED_500)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            )
        )
    )

    insights.controls.append(
        ft.Container(
            padding=padding_size,
            border=ft.border.all(1, border_color),
            border_radius=10,
            ink=True,
            on_click=lambda _: show_low_stock_items(),  # Show low stock dialog when clicked
            content=ft.Column(
                [
                    ft.Row(
                        spacing=3,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Low Stock Items", size=subtext_size, color=ft.colors.GREY_700),
                            ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, size=subtext_size, color=ft.colors.RED_500),
                        ]
                    ),
                    ft.Text(str(page.app_state['low_stock_items']), size=heading_size, weight=ft.FontWeight.BOLD),
                    ft.Text("Product", size=subtext_size)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            )
        )
    )

    # Revenue chart data
    revenue_data = [
        ("Apr 10", 120),
        ("Apr 11", 90),
        ("Apr 12", 160),
        ("Apr 13", 80),
        ("Apr 14", 140),
        ("Apr 15", 200),
    ]

    bar_groups = []
    bottom_labels = []

    for idx, (date, revenue) in enumerate(revenue_data):
        bar_groups.append(
            ft.BarChartGroup(
                x=idx,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=revenue,
                        width=30,
                        color=primary_color,
                        tooltip=f"{date}: ${revenue}",
                        border_radius=3,  # Slightly rounded corners
                    )
                ]
            )
        )

        bottom_labels.append(
            ft.ChartAxisLabel(
                value=idx,
                label=ft.Container(ft.Text(date, size=subtext_size - 2), padding=5),
            )
        )

    # Revenue chart with better styling and click functionality
    revenue_chart = ft.BarChart(
        bar_groups=bar_groups,
        border=ft.border.all(1, border_color),
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
        max_y=max([r for _, r in revenue_data]) + 50,
        interactive=True,
        expand=True,
        on_chart_event=lambda e: show_revenue_details(
            revenue_data[e.bar_group_index][0]) if e.event_type == "tap" else None,
    )

    revenue_section = ft.Container(
        margin=ft.margin.only(top=20, bottom=20),
        padding=padding_size,
        border=ft.border.all(1, border_color),
        border_radius=10,
        content=ft.Column(
            controls=[
                ft.Row([
                    ft.Text("Revenue This Week", size=subtext_size + 4, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Row([
                            ft.Container(width=10, height=10, bgcolor=primary_color, border_radius=5),
                            ft.Text("Daily Revenue", size=subtext_size - 2)
                        ], spacing=5),
                        padding=8
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=10),
                ft.Container(
                    height=250,
                    content=revenue_chart
                )
            ],
            spacing=5,
        ),
    )

    # Recent activity section
    recent_activity = ft.Container(
        margin=ft.margin.only(bottom=20),
        padding=padding_size,
        border=ft.border.all(1, border_color),
        border_radius=10,
        content=ft.Column([
            ft.Text("Recent Activity", size=subtext_size + 4, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.ListView(
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.SHOPPING_BAG, color=primary_color),
                        title=ft.Text("New sale completed"),
                        subtitle=ft.Text("Customer A - $85.99"),
                        trailing=ft.Text("10 min ago", size=subtext_size - 3, color=ft.colors.GREY_500),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.INVENTORY, color=ft.colors.AMBER_500),
                        title=ft.Text("Product C low in stock"),
                        subtitle=ft.Text("2 items remaining"),
                        trailing=ft.Text("2 hours ago", size=subtext_size - 3, color=ft.colors.GREY_500),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.PERSON_ADD, color=accent_color),
                        title=ft.Text("New customer registered"),
                        subtitle=ft.Text("Customer C joined"),
                        trailing=ft.Text("5 hours ago", size=subtext_size - 3, color=ft.colors.GREY_500),
                    ),
                ],
                height=180,
                spacing=0,
            )
        ])
    )

    # Set up page
    page.drawer = side_drawer

    # Return view with all components and dialogs included
    return ft.View(
        route="/",
        appbar=app_bar,
        controls=[
            side_drawer,
            header,
            cards,
            insights,
            revenue_section,
            recent_activity,
            # Include all dialogs in the controls list
            product_details_dialog,
            low_stock_dialog,
            order_dialog,
            revenue_details_dialog,
        ],
        scroll=ft.ScrollMode.AUTO,
    )