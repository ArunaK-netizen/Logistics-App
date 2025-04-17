import flet as ft
from components.home_view import home_view
from components.app_bar import app_bar_view
from components.inventory_view import inventory_view
from components.customers_view import customers_view
from components.insights_view import insights_view
from components.settings_view import settings_view
from components.sales_view import sales_view

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


    def route_change(e):
        route = page.route
        page.views.clear()

        if route == "/":
            page.views.append(home_view(page, app_bar, side_drawer))
        elif route == "/inventory":
            page.views.append(inventory_view(page, app_bar, side_drawer))
        elif route == "/sales":
            page.views.append(sales_view(page, app_bar, side_drawer))
        elif route == "/customers":
            page.views.append(customers_view(page, app_bar, side_drawer))
        elif route == "/insights":
            page.views.append(insights_view(page, app_bar, side_drawer))
        elif route == "/settings":
            page.views.append(settings_view(page, app_bar, side_drawer))

        page.update()

    page.on_route_change = route_change
    page.go("/")


ft.app(main)
