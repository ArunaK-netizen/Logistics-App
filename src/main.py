import flet as ft
from components.home_view import home_view
from components.app_bar import app_bar_view

def main(page: ft.Page):
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "/fonts/OpenSans-Regular.ttf",
        "Ntype": "https://raw.githubusercontent.com/Yokilleurs/NothingFonts/main/NType82-Regular.otf"
    }
    page.theme = ft.Theme(font_family="Ntype")
    page.scroll = ft.ScrollMode.AUTO
    last_saved_mode = ft.ThemeMode.LIGHT
    page.theme_mode = last_saved_mode


    side_drawer, notif_popup, app_bar = app_bar_view(page)



    products = [
        {"name": "Product A", "stock": 10},
        {"name": "Product B", "stock": 3},
        {"name": "Product C", "stock": 0},
    ]

    def inventory_view(page: ft.Page):
        page.controls.clear()
        page.appbar = ft.AppBar(title=ft.Text("Inventory"), bgcolor=ft.colors.SURFACE_VARIANT)
        items = []
        for idx, p in enumerate(products):
            items.append(
                ft.ListTile(
                    title=ft.Text(p["name"]),
                    subtitle=ft.Text(f"Stock: {p['stock']}"),
                    trailing=ft.Icon(ft.icons.ARROW_FORWARD),
                    on_click=lambda e, index=idx: page.go(f"/product/{index}")
                )
            )

        page.controls.append(ft.Column(controls=items))
        page.controls.append(ft.ElevatedButton("⬅️ Back to Home", on_click=lambda e: page.go("/")))
        page.update()

    def product_detail_view(page: ft.Page, product_id: int):
        page.controls.clear()
        product = products[product_id]
        page.appbar = ft.AppBar(title=ft.Text("Product Detail"), bgcolor=ft.colors.SURFACE_VARIANT)

        page.controls.append(
            ft.Column(
                controls=[
                    ft.Text(f"Product: {product['name']}", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Stock available: {product['stock']}"),
                    ft.ElevatedButton("⬅️ Back to Inventory", on_click=lambda e: page.go("/inventory"))
                ]
            )
        )
        page.update()




    def inventory_view():
        return ft.View("/inventory", controls=[ft.Text("Inventory Page")])

    def sales_view():
        return ft.View("/sales", controls=[ft.Text("Sales Page")])

    def customers_view():
        return ft.View("/customers", controls=[ft.Text("Customers Page")])

    def insights_view():
        return ft.View("/insights", controls=[ft.Text("Insights Page")])

    def settings_view():
        return ft.View("/settings", controls=[ft.Text("Settings Page")])

    def route_change(e):
        route = page.route
        page.views.clear()

        if route == "/":
            page.views.append(home_view(page, app_bar, side_drawer))
        elif route == "/inventory":
            page.views.append(inventory_view())
        elif route == "/sales":
            page.views.append(sales_view())
        elif route == "/customers":
            page.views.append(customers_view())
        elif route == "/insights":
            page.views.append(insights_view())
        elif route == "/settings":
            page.views.append(settings_view())

        page.update()

    page.on_route_change = route_change
    page.go("/")


ft.app(main)
