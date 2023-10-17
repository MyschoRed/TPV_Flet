import flet as ft
from flet import Page, Row, AppBar, Container, TextButton, ButtonStyle, colors
# from flet_core.types import WEB_BROWSER


from App.AppLayout import AppLayout
from App.BomImportForm import BomImportForm
# from App.SatatusMessage import StatusMessage


class TpvApp:
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.appbar = AppBar(
            bgcolor=colors.BLUE_300,
            title=ft.Text("TPVsystem"),
            actions=[
                Row(
                    [
                        Container(
                            content=TextButton(
                                text='Triedic suborov',
                                on_click=None,
                                style=ButtonStyle(color=colors.BLACK))),
                    ]
                )
            ]
        )
        self.page.appbar = self.appbar
        self.page.update()

    def build(self):
        # render content in layout
        app_layout = AppLayout(self, self.page)
        bom_import_form = BomImportForm()

        app_layout.alignment = ft.MainAxisAlignment.CENTER

        app_layout.page.overlay.append(bom_import_form.dialog_pick_file)
        app_layout.page.overlay.append(bom_import_form.dialog_select_path)

        app_layout.detail_frame.content = bom_import_form.bom_import_form
        app_layout.main_frame.content = bom_import_form.section_output_text
        app_layout.status_bar.content = bom_import_form.message_text
        return app_layout


if __name__ == "__main__":
    def main(page: Page):
        page.title = "Arack"
        page.window_width = 1200
        page.window_height = 800
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.bgcolor = colors.BLUE
        app = TpvApp(page).build()
        page.add(app)
        page.update()


    ft.app(target=main)
    # ft.app(target=main, view=WEB_BROWSER)
