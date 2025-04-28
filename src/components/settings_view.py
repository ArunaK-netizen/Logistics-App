import flet as ft
import json
import os


def settings_view(page, app_bar, side_drawer):
    # Responsive sizing
    heading_size = 30 if page.width > 800 else 22
    subtext_size = 16 if page.width > 800 else 13
    padding_size = 30 if page.width > 800 else 15

    # State variables
    show_save_button = False
    settings_changed = False
    
    # Default app settings - in a real app, these would be loaded from a database or file
    app_settings = {
        "appearance": {
            "theme": page.theme_mode.value,
            "dense_mode": False,
            "font_size": "Medium",
        },
        "notifications": {
            "email_notifications": True,
            "push_notifications": True,
            "order_updates": True,
            "inventory_alerts": True,
            "customer_activity": False,
        },
        "data": {
            "auto_backup": True,
            "backup_frequency": "Daily",
            "data_retention": "1 Year",
        },
        "account": {
            "username": "admin",
            "email": "admin@example.com",
            "last_login": "2023-05-10 09:45",
        }
    }
    
    # Header section
    header = ft.Container(
        padding=padding_size,
        content=ft.Column([
            ft.Text("Settings", size=heading_size),
            ft.Text("Configure your application preferences", size=subtext_size),
        ])
    )
    
    # Create tabs for different settings categories
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Appearance",
                icon=ft.icons.PALETTE,
                content=ft.Container(
                    padding=padding_size,
                    content=ft.Column([
                        ft.Text("Theme Settings", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.DARK_MODE),
                            title=ft.Text("App Theme"),
                            subtitle=ft.Text("Change the application theme"),
                            trailing=ft.Dropdown(
                                value=app_settings["appearance"]["theme"],
                                options=[
                                    ft.dropdown.Option("LIGHT", "Light Mode"),
                                    ft.dropdown.Option("DARK", "Dark Mode"),
                                    ft.dropdown.Option("SYSTEM", "System Default"),
                                ],
                                width=150,
                                on_change=lambda e: change_theme(e.control.value),
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.TEXT_FORMAT),
                            title=ft.Text("Font Size"),
                            subtitle=ft.Text("Adjust the application font size"),
                            trailing=ft.Dropdown(
                                value=app_settings["appearance"]["font_size"],
                                options=[
                                    ft.dropdown.Option("Small"),
                                    ft.dropdown.Option("Medium"),
                                    ft.dropdown.Option("Large"),
                                ],
                                width=150,
                                on_change=lambda e: (toggle_settings_changed(True), update_appearance_settings("font_size", e.control.value)),
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.VIEW_COMPACT),
                            title=ft.Text("Dense Mode"),
                            subtitle=ft.Text("Compact view with more content"),
                            trailing=ft.Switch(
                                value=app_settings["appearance"]["dense_mode"],
                                on_change=lambda e: (toggle_settings_changed(True), update_appearance_settings("dense_mode", e.control.value)),
                            ),
                        ),
                        ft.Container(height=20),
                        ft.Text("Preview", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            padding=20,
                            height=150,
                            border=ft.border.all(1, ft.colors.GREY_400),
                            border_radius=10,
                            content=ft.Column([
                                ft.Text("This is how content will appear", size=subtext_size + (0 if app_settings["appearance"]["font_size"] == "Medium" else (2 if app_settings["appearance"]["font_size"] == "Large" else -2))),
                                ft.Container(height=10),
                                ft.Row([
                                    ft.ElevatedButton("Primary Button"),
                                    ft.OutlinedButton("Secondary Button"),
                                ]),
                                ft.Container(height=10),
                                ft.TextField(
                                    label="Sample Input Field",
                                    hint_text="Enter text here",
                                    dense=app_settings["appearance"]["dense_mode"],
                                ),
                            ]),
                        ),
                    ]),
                ),
            ),
            ft.Tab(
                text="Notifications",
                icon=ft.icons.NOTIFICATIONS,
                content=ft.Container(
                    padding=padding_size,
                    content=ft.Column([
                        ft.Text("Notification Settings", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.EMAIL),
                            title=ft.Text("Email Notifications"),
                            subtitle=ft.Text("Receive notifications via email"),
                            trailing=ft.Switch(
                                value=app_settings["notifications"]["email_notifications"],
                                on_change=lambda e: (toggle_settings_changed(True), update_notification_settings("email_notifications", e.control.value)),
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.NOTIFICATIONS_ACTIVE),
                            title=ft.Text("Push Notifications"),
                            subtitle=ft.Text("Receive in-app notifications"),
                            trailing=ft.Switch(
                                value=app_settings["notifications"]["push_notifications"],
                                on_change=lambda e: (toggle_settings_changed(True), update_notification_settings("push_notifications", e.control.value)),
                            ),
                        ),
                        ft.Container(height=10),
                        ft.Text("Alert Types", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Checkbox(
                            label="Order Updates",
                            value=app_settings["notifications"]["order_updates"],
                            on_change=lambda e: (toggle_settings_changed(True), update_notification_settings("order_updates", e.control.value)),
                        ),
                        ft.Checkbox(
                            label="Inventory Alerts",
                            value=app_settings["notifications"]["inventory_alerts"],
                            on_change=lambda e: (toggle_settings_changed(True), update_notification_settings("inventory_alerts", e.control.value)),
                        ),
                        ft.Checkbox(
                            label="Customer Activity",
                            value=app_settings["notifications"]["customer_activity"],
                            on_change=lambda e: (toggle_settings_changed(True), update_notification_settings("customer_activity", e.control.value)),
                        ),
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "Test Notification",
                            icon=ft.icons.SEND,
                            on_click=lambda e: test_notification(),
                        ),
                    ]),
                ),
            ),
            ft.Tab(
                text="Data Management",
                icon=ft.icons.STORAGE,
                content=ft.Container(
                    padding=padding_size,
                    content=ft.Column([
                        ft.Text("Data Settings", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.BACKUP),
                            title=ft.Text("Automatic Backups"),
                            subtitle=ft.Text("Regularly back up your data"),
                            trailing=ft.Switch(
                                value=app_settings["data"]["auto_backup"],
                                on_change=lambda e: (toggle_settings_changed(True), update_data_settings("auto_backup", e.control.value)),
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.TIMER),
                            title=ft.Text("Backup Frequency"),
                            subtitle=ft.Text("How often to create backups"),
                            trailing=ft.Dropdown(
                                value=app_settings["data"]["backup_frequency"],
                                options=[
                                    ft.dropdown.Option("Daily"),
                                    ft.dropdown.Option("Weekly"),
                                    ft.dropdown.Option("Monthly"),
                                ],
                                width=150,
                                disabled=not app_settings["data"]["auto_backup"],
                                on_change=lambda e: (toggle_settings_changed(True), update_data_settings("backup_frequency", e.control.value)),
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.AUTO_DELETE),
                            title=ft.Text("Data Retention"),
                            subtitle=ft.Text("How long to keep historical data"),
                            trailing=ft.Dropdown(
                                value=app_settings["data"]["data_retention"],
                                options=[
                                    ft.dropdown.Option("1 Month"),
                                    ft.dropdown.Option("6 Months"),
                                    ft.dropdown.Option("1 Year"),
                                    ft.dropdown.Option("Forever"),
                                ],
                                width=150,
                                on_change=lambda e: (toggle_settings_changed(True), update_data_settings("data_retention", e.control.value)),
                            ),
                        ),
                        ft.Container(height=20),
                        ft.Row([
                            ft.ElevatedButton(
                                "Export All Data",
                                icon=ft.icons.DOWNLOAD,
                                on_click=lambda e: export_data(),
                            ),
                            ft.ElevatedButton(
                                "Backup Now",
                                icon=ft.icons.BACKUP,
                                on_click=lambda e: backup_now(),
                            ),
                        ]),
                        ft.Container(height=20),
                        ft.Text("Data Import", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Row([
                            ft.FilledButton(
                                "Import Data",
                                icon=ft.icons.UPLOAD_FILE,
                                on_click=lambda e: import_data(),
                            ),
                            ft.OutlinedButton(
                                "Restore from Backup",
                                icon=ft.icons.RESTORE,
                                on_click=lambda e: restore_backup(),
                            ),
                        ]),
                    ]),
                ),
            ),
            ft.Tab(
                text="Account",
                icon=ft.icons.PERSON,
                content=ft.Container(
                    padding=padding_size,
                    content=ft.Column([
                        ft.Text("Account Information", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.PERSON),
                            title=ft.Text("Username"),
                            subtitle=ft.Text(app_settings["account"]["username"]),
                            trailing=ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip="Edit Username",
                                on_click=lambda e: edit_account_field("username"),
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.EMAIL),
                            title=ft.Text("Email Address"),
                            subtitle=ft.Text(app_settings["account"]["email"]),
                            trailing=ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip="Edit Email",
                                on_click=lambda e: edit_account_field("email"),
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.ACCESS_TIME),
                            title=ft.Text("Last Login"),
                            subtitle=ft.Text(app_settings["account"]["last_login"]),
                        ),
                        ft.Container(height=20),
                        ft.Text("Security", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.ElevatedButton(
                            "Change Password",
                            icon=ft.icons.LOCK,
                            on_click=lambda e: change_password(),
                        ),
                        ft.Container(height=20),
                        ft.Text("Danger Zone", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Container(
                            padding=20,
                            border=ft.border.all(1, ft.colors.RED_400),
                            border_radius=10,
                            content=ft.Column([
                                ft.Row([
                                    ft.Text("Delete Account", color=ft.colors.RED),
                                    ft.Text("This action cannot be undone", size=subtext_size - 2, color=ft.colors.GREY_600),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Container(height=10),
                                ft.OutlinedButton(
                                    "Delete My Account",
                                    icon=ft.icons.DELETE_FOREVER,
                                    style=ft.ButtonStyle(
                                        color=ft.colors.RED,
                                        shape=ft.RoundedRectangleBorder(radius=5),
                                    ),
                                    on_click=lambda e: confirm_delete_account(),
                                ),
                            ]),
                        ),
                    ]),
                ),
            ),
            ft.Tab(
                text="About",
                icon=ft.icons.INFO,
                content=ft.Container(
                    padding=padding_size,
                    content=ft.Column([
                        ft.Text("Application Information", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.APPS),
                            title=ft.Text("Application Name"),
                            subtitle=ft.Text("Business Management System"),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.NEW_RELEASES),
                            title=ft.Text("Version"),
                            subtitle=ft.Text("1.0.0"),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.COPYRIGHT),
                            title=ft.Text("License"),
                            subtitle=ft.Text("© 2023 Your Company"),
                        ),
                        ft.Container(height=20),
                        ft.Text("Credits", size=subtext_size + 2, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.CODE),
                            title=ft.Text("Powered By"),
                            subtitle=ft.Text("Flet (Flutter + Python)"),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.PEOPLE),
                            title=ft.Text("Developers"),
                            subtitle=ft.Text("The Development Team"),
                        ),
                        ft.Container(height=20),
                        ft.Row([
                            ft.ElevatedButton(
                                "Check for Updates",
                                icon=ft.icons.UPDATE,
                                on_click=lambda e: check_for_updates(),
                            ),
                            ft.OutlinedButton(
                                "View License",
                                icon=ft.icons.DESCRIPTION,
                                on_click=lambda e: view_license(),
                            ),
                        ]),
                    ]),
                ),
            ),
        ],
        expand=1,
    )
    
    # Confirmation dialog for save changes
    save_confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Save Changes"),
        content=ft.Text("Your settings have been saved successfully."),
        actions=[
            ft.TextButton("OK", on_click=lambda e: close_dialog(save_confirm_dialog)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    # Confirmation dialog for account deletion
    delete_account_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Account Deletion"),
        content=ft.Column([
            ft.Text("Are you sure you want to delete your account? This action cannot be undone."),
            ft.Container(height=20),
            ft.TextField(label="Enter your password to confirm", password=True),
        ], width=400, tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(delete_account_dialog)),
            ft.ElevatedButton(
                "Delete My Account",
                icon=ft.icons.DELETE_FOREVER,
                style=ft.ButtonStyle(
                    color=ft.colors.RED,
                    bgcolor=ft.colors.RED_50,
                ),
                on_click=lambda e: delete_account(),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    # Dialog for editing account fields
    edit_account_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Account Information"),
        content=ft.Column([
            ft.TextField(label="Enter new value", value=""),
        ], width=400, tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(edit_account_dialog)),
            ft.ElevatedButton(
                "Save",
                on_click=lambda e: save_account_field(),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    # Dialog for changing password
    change_password_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Change Password"),
        content=ft.Column([
            ft.TextField(label="Current Password", password=True),
            ft.TextField(label="New Password", password=True),
            ft.TextField(label="Confirm New Password", password=True),
        ], width=400, tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(change_password_dialog)),
            ft.ElevatedButton(
                "Change Password",
                on_click=lambda e: update_password(),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    # License info dialog
    license_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("License Information"),
        content=ft.Column([
            ft.Text("Business Management System", weight=ft.FontWeight.BOLD),
            ft.Text("Version 1.0.0"),
            ft.Container(height=10),
            ft.Text("© 2023 Your Company. All rights reserved."),
            ft.Container(height=10),
            ft.Text(
                "This software is provided 'as-is', without any express or implied warranty. "
                "In no event will the authors be held liable for any damages arising from the use of this software."
            ),
        ], width=400, scroll=ft.ScrollMode.AUTO, height=300),
        actions=[
            ft.TextButton("Close", on_click=lambda e: close_dialog(license_dialog)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    # Save button (appears when changes are made)
    save_button = ft.FloatingActionButton(
        icon=ft.icons.SAVE,
        text="Save Changes",
        visible=show_save_button,
        on_click=lambda e: save_settings(),
    )
    
    # Define all functions
    
    def toggle_settings_changed(changed):
        nonlocal settings_changed, show_save_button
        settings_changed = changed
        show_save_button = changed
        save_button.visible = changed
        page.update()
    
    def close_dialog(dialog):
        dialog.open = False
        page.update()
    
    def save_settings():
        # In a real app, this would save to a database or file
        page.dialog = save_confirm_dialog
        save_confirm_dialog.open = True
        toggle_settings_changed(False)
        page.update()
    
    def change_theme(theme_value):
        app_settings["appearance"]["theme"] = theme_value
        toggle_settings_changed(True)
        
        # Actually change the theme
        if theme_value == "LIGHT":
            page.theme_mode = ft.ThemeMode.LIGHT
        elif theme_value == "DARK":
            page.theme_mode = ft.ThemeMode.DARK
        else:  # SYSTEM
            page.theme_mode = ft.ThemeMode.SYSTEM
            
        page.update()
    
    def update_appearance_settings(key, value):
        app_settings["appearance"][key] = value
        page.update()
    
    def update_notification_settings(key, value):
        app_settings["notifications"][key] = value
        page.update()
    
    def update_data_settings(key, value):
        app_settings["data"][key] = value
        # If auto_backup is toggled, update the backup frequency dropdown state
        if key == "auto_backup":
            tabs.tabs[2].content.content.controls[3].trailing.disabled = not value
        page.update()
    
    def test_notification():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("This is a test notification"),
            action="Dismiss",
        )
        page.snack_bar.open = True
        page.update()
    
    def export_data():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Data exported successfully"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()
    
    def backup_now():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Backup created successfully"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()
    
    def import_data():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Data import would open a file picker in a real app"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()
    
    def restore_backup():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Restore from backup would show backup list in a real app"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()
    
    def edit_account_field(field):
        # Store the field being edited
        edit_account_dialog.field_to_edit = field
        
        # Set the current value
        edit_account_dialog.content.controls[0].value = app_settings["account"][field]
        
        # Update the dialog title
        edit_account_dialog.title = ft.Text(f"Edit {field.title()}")
        
        # Show the dialog
        page.dialog = edit_account_dialog
        edit_account_dialog.open = True
        page.update()
    
    def save_account_field():
        # Get the field and new value
        field = edit_account_dialog.field_to_edit
        new_value = edit_account_dialog.content.controls[0].value
        
        # Update the settings
        app_settings["account"][field] = new_value
        
        # Update the UI
        for tab in tabs.tabs:
            if tab.text == "Account":
                # Find the right ListTile
                for control in tab.content.content.controls:
                    if isinstance(control, ft.ListTile) and control.title.value == field.title():
                        control.subtitle.value = new_value
                        break
        
        # Close the dialog
        close_dialog(edit_account_dialog)
        
        # Show confirmation
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"{field.title()} updated successfully"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()
    
    def change_password():
        page.dialog = change_password_dialog
        change_password_dialog.open = True
        page.update()
    
    def update_password():
        # In a real app, this would validate and update the password
        # For this demo, we'll just show a success message
        close_dialog(change_password_dialog)
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Password changed successfully"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()
    
    def confirm_delete_account():
        page.dialog = delete_account_dialog
        delete_account_dialog.open = True
        page.update()
    
    def delete_account():
        # In a real app, this would delete the account
        # For this demo, we'll just show a message
        close_dialog(delete_account_dialog)
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Account deletion would be processed in a real app"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()
    
    def check_for_updates():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("You are using the latest version"),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()
    
    def view_license():
        page.dialog = license_dialog
        license_dialog.open = True
        page.update()
    
    # Update UI based on window resize
    def on_resize(e):
        # Update responsive elements based on new width
        nonlocal heading_size, subtext_size, padding_size
        heading_size = 30 if page.width > 800 else 22
        subtext_size = 16 if page.width > 800 else 13
        padding_size = 30 if page.width > 800 else 15
        
        # Update header text sizes
        header.content.controls[0].size = heading_size
        header.content.controls[1].size = subtext_size
        
        page.update()
    
    page.on_resize = on_resize
    page.drawer = side_drawer
    
    # Return the complete view
    return ft.View(
        route="/settings",
        appbar=app_bar,
        controls=[
            side_drawer,
            header,
            tabs,
            save_button,
            # Include all dialogs
            save_confirm_dialog,
            delete_account_dialog,
            edit_account_dialog,
            change_password_dialog,
            license_dialog,
        ],
        scroll=ft.ScrollMode.AUTO,
        floating_action_button=save_button,
    )