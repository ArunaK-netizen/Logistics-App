import flet as ft

def inventory_view(page,app_bar, side_drawer):
    page.drawer = side_drawer
    return ft.View(
        route="/inventory",
        appbar=app_bar,
        controls=[side_drawer,
            ft.Container(
                content=ft.Column([
                    ft.Text("Inventory Page", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Manage your products here", size=16),
                ]),
                padding=20
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )