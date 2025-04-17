import flet as ft



def customers_view(page,app_bar, side_drawer):
    page.drawer = side_drawer
    return ft.View(
        route="/customers",
        appbar=app_bar,
        controls=[side_drawer,
            ft.Container(
                content=ft.Column([
                    ft.Text("Customers Page", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Manage your customers here", size=16),
                    # Add more inventory-related controls here
                ]),
                padding=20
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )