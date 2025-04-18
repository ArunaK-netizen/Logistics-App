import flet as ft


def insights_view(page, app_bar, side_drawer):
    heading_size = 30 if page.width > 800 else 22
    subtext_size = 16 if page.width > 800 else 13
    padding_size = 30 if page.width > 800 else 15

    # Header section
    header = ft.Container(
        padding=padding_size,
        content=ft.Column([
            ft.Text("Business Insights", size=heading_size),
            ft.Text("Analyze your business performance and trends", size=subtext_size),
        ])
    )

    # Time period selector
    time_selector = ft.Container(
        padding=ft.padding.only(left=padding_size, right=padding_size),
        content=ft.Row([
            ft.Text("Time Period:", size=subtext_size),
            ft.Dropdown(
                width=150,
                options=[
                    ft.dropdown.Option("Last 7 days"),
                    ft.dropdown.Option("Last 30 days"),
                    ft.dropdown.Option("Last 90 days"),
                    ft.dropdown.Option("This year"),
                ],
                value="Last 30 days",
            )
        ], alignment=ft.MainAxisAlignment.END)
    )

    # Key metrics cards
    metrics_cards = ft.ResponsiveRow([
        ft.Container(
            col={"sm": 6, "md": 3, "lg": 3},
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column([
                ft.Text("Total Revenue", size=subtext_size, color=ft.colors.GREY_700),
                ft.Text("$3,249.96", size=heading_size),
                ft.Row([
                    ft.Text("↑ 18.5%", size=subtext_size, color=ft.colors.GREEN_500),
                    ft.Text(" vs previous period", size=subtext_size - 2, color=ft.colors.GREY_500)
                ])
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
        ),
        ft.Container(
            col={"sm": 6, "md": 3, "lg": 3},
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column([
                ft.Text("Orders", size=subtext_size, color=ft.colors.GREY_700),
                ft.Text("42", size=heading_size),
                ft.Row([
                    ft.Text("↑ 12.2%", size=subtext_size, color=ft.colors.GREEN_500),
                    ft.Text(" vs previous period", size=subtext_size - 2, color=ft.colors.GREY_500)
                ])
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
        ),
        ft.Container(
            col={"sm": 6, "md": 3, "lg": 3},
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column([
                ft.Text("Avg Order Value", size=subtext_size, color=ft.colors.GREY_700),
                ft.Text("$77.38", size=heading_size),
                ft.Row([
                    ft.Text("↑ 5.3%", size=subtext_size, color=ft.colors.GREEN_500),
                    ft.Text(" vs previous period", size=subtext_size - 2, color=ft.colors.GREY_500)
                ])
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
        ),
        ft.Container(
            col={"sm": 6, "md": 3, "lg": 3},
            padding=padding_size,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            content=ft.Column([
                ft.Text("Active Customers", size=subtext_size, color=ft.colors.GREY_700),
                ft.Text("26", size=heading_size),
                ft.Row([
                    ft.Text("↑ 8.3%", size=subtext_size, color=ft.colors.GREEN_500),
                    ft.Text(" vs previous period", size=subtext_size - 2, color=ft.colors.GREY_500)
                ])
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
        )
    ])

    # Sales chart section
    sales_data = [
        ("Week 1", 420),
        ("Week 2", 390),
        ("Week 3", 620),
        ("Week 4", 580),
    ]

    bar_groups = []
    bottom_labels = []

    for idx, (date, revenue) in enumerate(sales_data):
        bar_groups.append(
            ft.BarChartGroup(
                x=idx,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=revenue,
                        width=35,
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

    sales_chart = ft.Container(
        padding=padding_size,
        content=ft.Column([
            ft.Row([
                ft.Text("Monthly Sales Trend", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                ft.Container(
                    ft.Row([
                        ft.Container(width=10, height=10, bgcolor=ft.colors.BLUE_500, border_radius=5),
                        ft.Text("Revenue", size=subtext_size - 2)
                    ]),
                    padding=8
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=ft.BarChart(
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
                    max_y=700,
                    interactive=True,
                    expand=True,
                    height=250
                ),
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=10,
                padding=10
            )
        ])
    )

    # Bottom sections - Product performance and customer insights
    bottom_section = ft.ResponsiveRow([
        # Top Products section
        ft.Container(
            col={"sm": 12, "md": 6, "lg": 6},
            padding=padding_size,
            content=ft.Column([
                ft.Text("Top Products", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Product")),
                            ft.DataColumn(ft.Text("Units Sold")),
                            ft.DataColumn(ft.Text("Revenue"), numeric=True),
                        ],
                        rows=[
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Product A")),
                                ft.DataCell(ft.Text("28")),
                                ft.DataCell(ft.Text("$840.00")),
                            ]),
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Product B")),
                                ft.DataCell(ft.Text("23")),
                                ft.DataCell(ft.Text("$690.00")),
                            ]),
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Product C")),
                                ft.DataCell(ft.Text("19")),
                                ft.DataCell(ft.Text("$570.00")),
                            ]),
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Product D")),
                                ft.DataCell(ft.Text("15")),
                                ft.DataCell(ft.Text("$450.00")),
                            ]),
                        ],
                    ),
                    border=ft.border.all(1, ft.colors.GREY_400),
                    border_radius=10,
                    padding=10
                )
            ])
        ),

        # Customer insights section
        ft.Container(
            col={"sm": 12, "md": 6, "lg": 6},
            padding=padding_size,
            content=ft.Column([
                ft.Text("Customer Insights", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("New Customers", size=subtext_size, color=ft.colors.GREY_700),
                                    ft.Text("14", size=heading_size - 6),
                                    ft.Text("↑ 16.7%", size=subtext_size - 2, color=ft.colors.GREEN_500),
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                                expand=True,
                                border=ft.border.all(1, ft.colors.GREY_300),
                                border_radius=10,
                                padding=10
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Repeat Customers", size=subtext_size, color=ft.colors.GREY_700),
                                    ft.Text("12", size=heading_size - 6),
                                    ft.Text("↑ 9.1%", size=subtext_size - 2, color=ft.colors.GREEN_500),
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                                expand=True,
                                border=ft.border.all(1, ft.colors.GREY_300),
                                border_radius=10,
                                padding=10
                            ),
                        ]),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Customer Retention Rate", size=subtext_size, color=ft.colors.GREY_700),
                                ft.ProgressBar(value=0.68, width=280, height=15, bgcolor=ft.colors.GREY_300,
                                               color=ft.colors.BLUE_400),
                                ft.Text("68%", size=subtext_size),
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5),
                            expand=True,
                            border=ft.border.all(1, ft.colors.GREY_300),
                            border_radius=10,
                            padding=15
                        ),
                    ]),
                    border=ft.border.all(1, ft.colors.GREY_400),
                    border_radius=10,
                    padding=10
                )
            ])
        ),
    ])

    page.drawer = side_drawer

    return ft.View(
        route="/insights",
        appbar=app_bar,
        controls=[
            side_drawer,
            header,
            time_selector,
            metrics_cards,
            sales_chart,
            bottom_section
        ],
        scroll=ft.ScrollMode.AUTO,
    )