import flet as ft

def home_view(page, app_bar, side_drawer):
    heading_size = 30 if page.width > 800 else 22
    subtext_size = 16 if page.width > 800 else 13
    padding_size = 30 if page.width > 800 else 15


    header = ft.Container(
        padding=padding_size,
        content=ft.Column([
            ft.Text("Dashboard", size=heading_size),
            ft.Text("Welcome back, here's your store overview", size=subtext_size),
        ])
    )

    cards = ft.ResponsiveRow([
        ft.Container(
            col={"sm": 4, "md": 4, "lg": 4},
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ADDCHART),
                    ft.Text("Manage Products", size=subtext_size),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ),
        ft.Container(
            col={"sm": 4, "md": 4, "lg": 4},
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.GRAPHIC_EQ, color=ft.colors.GREEN_500),
                    ft.Text("View Customers", size=subtext_size),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ),
        ft.Container(
            col={"sm": 4, "md": 4, "lg": 4},
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.SHOPPING_CART),
                    ft.Text("View All Sales", size=subtext_size),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    ])

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
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column(
                [
                    ft.Row(
                        spacing=5,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Total Sales", size=subtext_size, color=ft.colors.GREY_700),
                            ft.Icon(ft.Icons.CURRENCY_POUND, size=subtext_size + 2, color=ft.colors.GREEN_900),
                        ]
                    ),
                    ft.Text("$249.96", size=heading_size),
                    ft.Text("↑ 12.5%", size=subtext_size, color=ft.colors.GREEN_500)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=60,
            )
        )
    )

    insights.controls.append(
        ft.Container(
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column(
                [
                    ft.Row(
                        spacing=5,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Total Orders", size=subtext_size, color=ft.colors.GREY_700),
                            ft.Icon(ft.Icons.SHOPPING_CART_CHECKOUT, size=subtext_size + 2,
                                    color=ft.colors.BLUE_GREY_500),
                        ]
                    ),
                    ft.Text("3", size=heading_size),
                    ft.Text("↑ 8.2%", size=subtext_size, color=ft.colors.GREEN_500)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=60,
            )
        )
    )

    insights.controls.append(
        ft.Container(
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column(
                [
                    ft.Row(
                        spacing=5,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Prod. in Stock", size=subtext_size, color=ft.colors.GREY_700),
                            ft.Icon(ft.Icons.SHOPPING_BAG, size=subtext_size + 2, color=ft.colors.AMBER_500),
                        ]
                    ),
                    ft.Text("3", size=heading_size),
                    ft.Text("↓ 3.1%", size=subtext_size, color=ft.colors.RED_500)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=60,
            )
        )
    )

    insights.controls.append(
        ft.Container(
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column(
                [
                    ft.Row(
                        spacing=3,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Low Stock Items", size=subtext_size, color=ft.colors.GREY_700),
                            ft.Icon(ft.Icons.WARNING, size=subtext_size, color=ft.colors.RED_500),
                        ]
                    ),
                    ft.Text("1", size=heading_size),
                    ft.Text("Product", size=subtext_size)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=60,
            )
        )
    )

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
                        color=ft.colors.BLUE_500,
                        tooltip=f"{date}: ${revenue}",
                        border_radius=0,
                    )
                ]
            )
        )

        bottom_labels.append(
            ft.ChartAxisLabel(
                value=idx,
                label=ft.Container(ft.Text(date), padding=5),
            )
        )

    revenue_chart = ft.BarChart(
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
        max_y=max([r for _, r in revenue_data]) + 20,
        interactive=True,
        expand=True,
    )

    revenue_section = ft.Container(
        content=ft.Column(
            controls=[ft.Text("Revenue This Week", size=24, weight=ft.FontWeight.BOLD), revenue_chart]
        ),
        padding=20,
    )

    page.drawer = side_drawer


    return ft.View(
        route="/",
        appbar=app_bar,
        controls=[
            side_drawer,
            header,
            cards,
            insights,
            revenue_section
        ],
        scroll=ft.ScrollMode.AUTO,
    )
