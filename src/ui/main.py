import flet as ft


def main(page: ft.Page):
    page.title = "System Catalyst"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Row(
            [
                ft.Text(
                    "Welcome to System Catalyst", size=30, weight=ft.FontWeight.BOLD
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
