import flet as ft



def insights_view(page,app_bar, side_drawer):
    page.drawer = side_drawer
    return ft.View(
        route="/insights",
        appbar=app_bar,
        controls=[side_drawer,
            ft.Container(
                content=ft.Column([
                    ft.Text("Insights Page", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Manage your insights here", size=16),
                    # Add more inventory-related controls here
                ]),
                padding=20
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )