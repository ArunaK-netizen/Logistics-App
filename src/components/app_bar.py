import flet as ft



def app_bar_view(page):
    notifications = ["Low stock on Product A", "New sale on Product B", "Customer C requested a refund"]


    def clear_all_notifications():
        notifications.clear()

        notif_popup.content.controls[2:] = [
            ft.Text("No notifications", size=14, color=ft.colors.GREY_500)
        ]

        # Also update the badge count on the bell icon
        bell_icon.controls[1].content.value = "0"

        page.update()

    def handle_drawer_change(e):
        index = e.control.selected_index
        routes = ["/", "/inventory", "/sales", "/customers", "/insights", "/settings"]
        page.go(routes[index])

    side_drawer = ft.NavigationDrawer(
        selected_index=0,
        on_change=handle_drawer_change,
        controls=[
            ft.Container(height=50),
            ft.Container(ft.Text("Menu", size=18, weight=ft.FontWeight.BOLD), padding=10),
            ft.Divider(),
            ft.NavigationDrawerDestination(icon=ft.icons.HOME, label="Dashboard"),
            ft.NavigationDrawerDestination(icon=ft.icons.INVENTORY, label="Inventory"),
            ft.NavigationDrawerDestination(icon=ft.icons.SHOPPING_CART, label="Sales"),
            ft.NavigationDrawerDestination(icon=ft.icons.HOME, label="Customers"),
            ft.NavigationDrawerDestination(icon=ft.icons.INSIGHTS, label="Insights"),
            ft.NavigationDrawerDestination(icon=ft.icons.SETTINGS, label="Settings"),
            ft.Container(expand=True),
            ft.Divider(),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.ACCOUNT_CIRCLE),
                            title=ft.Text("Login / Signup"),
                            subtitle=ft.Text("Access your account"),
                        )
                    ]
                ),
                padding=10,
            )
        ]
    )



    def open_side_menu(e=None):
        side_drawer.open = True
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
        last_saved_mode = page.theme_mode
        page.update()


    def toggle_notifications_popup(e=None, ):
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

    return side_drawer,notif_popup, ft.AppBar(
            leading=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.MENU,
                        icon_size=24,
                        on_click=lambda e : open_side_menu(e),
                    ),

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

                ft.IconButton(
                    icon=ft.icons.DARK_MODE,
                    icon_color=ft.colors.GREY_700,
                    tooltip="Toggle Theme",
                    on_click=lambda e: toggle_theme()
                ),
                ft.IconButton(
                    icon=ft.icons.ACCOUNT_CIRCLE,
                    icon_color=ft.colors.GREY_700,
                    tooltip="Account"
                ),
            ]
        )