import flet as ft

app_bar = ft.AppBar(
    leading=ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.MENU,
                icon_size=24,
                on_click=open_side_menu,
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
        # 👤 Account icon
        ft.IconButton(
            icon=ft.icons.ACCOUNT_CIRCLE,
            icon_color=ft.colors.GREY_700,
            tooltip="Account"
        ),
    ]
)

