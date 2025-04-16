import flet as ft

def main(page: ft.Page):
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "/fonts/OpenSans-Regular.ttf",
        "Ntype": "https://raw.githubusercontent.com/Yokilleurs/NothingFonts/main/NType82-Regular.otf"
    }
    page.theme = ft.Theme(font_family="Ntype")
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    notifications = ["Low stock on Product A", "New sale on Product B", "Customer C requested a refund"]

    def clear_all_notifications():
        notifications.clear()

        notif_popup.content.controls[2:] = [
            ft.Text("No notifications", size=14, color=ft.colors.GREY_500)
        ]

        # Also update the badge count on the bell icon
        bell_icon.controls[1].content.value = "0"

        page.update()

    notif_popup = ft.Container(
        visible=False,
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Notifications", size=15, weight=ft.FontWeight.BOLD),
                            ft.TextButton(
                                text="Clear All",
                                style=ft.ButtonStyle(
                                    padding=0,
                                ),
                                on_click=lambda e: clear_all_notifications(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=10,
                )

                ,

                ft.Divider(),
                *([ft.Text(notif, size=14) for notif in notifications] if notifications
                  else [ft.Text("No notifications", size=14, color=ft.colors.GREY_500)])
            ],
            spacing=10,
        )
        ,
        bgcolor=ft.colors.WHITE,
        border_radius=8,
        shadow=ft.BoxShadow(
            color=ft.colors.BLACK12,
            blur_radius=4,
            spread_radius=1,
            offset=ft.Offset(0, 2),
        ),
        padding=10,
        width=250,
    )

    page.overlay.append(notif_popup)


    def toggle_theme():
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        page.update()

    def toggle_notifications_popup(e):
        notif_popup.right = 10
        notif_popup.top = 5
        notif_popup.visible = not notif_popup.visible
        page.update()

    bell_icon = ft.Stack(
        controls=[
            ft.IconButton(
                icon=ft.icons.NOTIFICATIONS,
                icon_size=24,
                tooltip="View notifications",
                on_click=toggle_notifications_popup
            ),
            ft.Container(
                content=ft.Text(str(len(notifications)), size=12, color=ft.colors.WHITE),
                bgcolor=ft.colors.RED,
                width=18,
                height=18,
                alignment=ft.alignment.center,
                border_radius=10,
                right=0,
                top=0,
            )
        ],
        width=40,
        height=40,
    )

    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=50),
            ft.Container(ft.Text("Menu", size=18, weight=ft.FontWeight.BOLD), padding=10)
            ,
            ft.Divider(),
            ft.NavigationDrawerDestination(
                icon=ft.icons.HOME,
                label="Dashboard",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.icons.INVENTORY,
                label="Inventory",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.icons.SHOPPING_CART,
                label="Sales",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.icons.HOME,
                label="Customers",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.icons.INSIGHTS,
                label="Insights",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.icons.SETTINGS,
                label="Settings",
            ),

            ft.Container(expand=True),

            ft.Divider(),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.ACCOUNT_CIRCLE),
                            title=ft.Text("Login / Signup"),
                            subtitle=ft.Text("Access your account"),
                            # on_click=lambda e: page.snack_bar.open("Login action")
                        )
                    ]
                ),
                padding=10
            )
        ]
    )

    def open_side_menu(e=None):
        page.drawer.open = True
        page.update()




    def update_layout(e=None):
        page.controls.clear()

        width = page.width

        heading_size = 30 if width > 800 else 22
        subtext_size = 16 if width > 800 else 13
        padding_size = 30 if width > 800 else 15

        page.appbar = ft.AppBar(
            leading=ft.Row(
    controls=[
        ft.IconButton(
            icon=ft.icons.MENU,
            icon_size=24,
            on_click=lambda e : open_side_menu()
        ),

        # Search bar
        ft.Container(
            content=ft.TextField(
                hint_text="Search...",
                height=40,
                border_radius=20,
                dense=True,
                filled=True,
                fill_color=ft.colors.SURFACE,
                content_padding=10,
                prefix_icon=ft.icons.SEARCH,
            ),
            margin=ft.margin.only(right=10),
            width=200
        )
    ],
    alignment=ft.MainAxisAlignment.START,
    vertical_alignment=ft.CrossAxisAlignment.CENTER
),
            leading_width=40,
            center_title=False,
            bgcolor=ft.colors.SURFACE_CONTAINER_HIGHEST,
            actions=[

                        bell_icon,




                # 🌙/☀️ Theme toggle
                ft.IconButton(
                    icon=ft.icons.DARK_MODE,
                    icon_color=ft.colors.GREY_700,
                    tooltip="Toggle Theme",
                    on_click=lambda e: toggle_theme()
                ),
                # 👤 Account icon
                ft.IconButton(
                    icon=ft.icons.ACCOUNT_CIRCLE,
                    icon_color=ft.colors.GREY_700,
                    tooltip="Account"
                ),
            ]
        )

        page.add(
            ft.Container(
                padding=padding_size,
                content=ft.Column([
                    ft.Text("Dashboard", size=heading_size),
                    ft.Text("Welcome back, here's your store overview", size=subtext_size),
                ])
            )
        )

        page.add(
            ft.ResponsiveRow([
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
        )
        if width < 500:
            insights_item_width = width // 2
        elif width < 800:
            insights_item_width = width // 2
        else:
            insights_item_width = width // 2

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
                                ft.Icon(ft.Icons.SHOPPING_CART_CHECKOUT, size=subtext_size + 2, color=ft.colors.BLUE_GREY_500),
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
                        )
                        ,
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
                        ft.Text("Product", size=subtext_size),

                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=60,
                )
            )
        )
        page.add(insights)

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
            max_y=max([r for _, r in revenue_data]) + 20,
            interactive=True,
            expand=True,
        )

        page.add(ft.Text("Revenue This Week", size=24, weight=ft.FontWeight.BOLD))
        page.add(chart)
        page.update()

    update_layout()

    page.on_resize = update_layout

ft.app(main)
