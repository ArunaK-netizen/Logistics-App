import flet as ft



def settings_view(page,app_bar, side_drawer):
    page.drawer = side_drawer
    return ft.View(
        route="/settings",
        appbar=app_bar,
        controls=[side_drawer,
            ft.Container(
                content=ft.Column([
                    ft.Text("Settings Page", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Manage your settings here", size=16),
                ]),
                padding=20
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )