import flet as ft
from flet import colors

from App.ExcelHandler import load_excel_file, get_files_from_excel
from App.FolderGenerator import generate_path_list, folder_generator, save_path_to_db


class BomImportForm:
    def __init__(self):
        super().__init__()

        self.message_text = ft.Text(color=colors.BLACK, size=15)

        # načítanie BOM
        self.label_pick_file = ft.Text('Tabuľka kusovníka', color=colors.BLACK)
        self.btn_pick_file = ft.ElevatedButton(
            "Načítaj kusovník",
            bgcolor=colors.BLUE_300,
            color=colors.BLACK,
            width=400,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.dialog_pick_file.pick_files(
                allow_multiple=False
            ),
        )
        self.text_selected_file = ft.Text(color=colors.BLACK)
        self.dialog_pick_file = ft.FilePicker(on_result=self.pick_file_result)
        self.section_pick_file = ft.Container(
            margin=20,
            content=ft.Column(
                [
                    self.label_pick_file,
                    self.btn_pick_file,
                    self.text_selected_file
                ]
            )
        )

        # názov hárka
        self.label_sheet_name_input = ft.Text(value='Názov hárka', color=colors.BLACK)
        self.value_sheet_name_input = ft.TextField(value='Priecinky', color=colors.BLACK, content_padding=10, height=40)
        self.section_sheet_name_input = ft.Container(
            margin=20,
            content=ft.Column(
                [
                    self.label_sheet_name_input,
                    self.value_sheet_name_input,
                ]
            )
        )

        # načítanie adresára
        self.label_select_path = ft.Text('Zvoľ cestu k súborom opakovanej výroby', color=colors.BLACK)
        self.btn_select_path = ft.ElevatedButton(
            "Načítaj adresár",
            bgcolor=colors.BLUE_300,
            color=colors.BLACK,
            width=400,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
            icon=ft.icons.FOLDER,
            on_click=lambda _: self.dialog_select_path.get_directory_path(
                dialog_title='Vyber cestu k opakovanej výrobe'
            ),
        )
        self.text_selected_path = ft.Text(
            color=colors.BLACK,
            width=400,
            selectable=True,
            overflow=ft.TextOverflow.CLIP,
            max_lines=1
        )
        self.dialog_select_path = ft.FilePicker(on_result=self.pick_path_result)
        self.section_select_path = ft.Container(
            margin=20,
            content=ft.Column(
                [
                    self.label_select_path,
                    self.btn_select_path,
                    self.text_selected_path,
                ]
            )
        )

        # spracovanie formulára
        self.btn_confirm = ft.ElevatedButton(
            "Spracovať",
            bgcolor=colors.GREEN_600,
            color=colors.BLACK,
            width=400,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    radius=5)
            ),
            # icon=ft.icons.FOLDER,
            on_click=self.generate_folders,
        )

        # sekcie formulára
        self.confirm_btn_section = ft.Container(
            margin=20,
            content=self.btn_confirm)

        # formulár
        self.input_section = ft.Column(
            controls=[
                self.section_pick_file,
                self.section_sheet_name_input,
                self.section_select_path,
            ]
        )

        self.bom_import_form = ft.Column(
            spacing=150,
            controls=[
                self.input_section,
                self.confirm_btn_section
            ]
        )

        # výpis údajov
        self.cleared_path_list = []
        self.label_output_text = ft.Text(color=colors.BLACK)
        self.output_text = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[],
        )
        self.section_output_text = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[self.label_output_text,
                      ft.Container(
                          content=self.output_text,
                          margin=20)
                      ]
        )

    def pick_file_result(self, e: ft.FilePickerResultEvent):
        self.output_text.clean()
        self.output_text.update()

        if e.files is not None:
            file_type = e.files[0].name[-4:]
            if file_type.lower() == 'xlsx':
                self.text_selected_file.value = (", ".join(map(lambda f: f.name, e.files)))
                self.text_selected_file.update()
                self.message_text.value = 'Súbor úspešne načítaný!'
                self.message_text.color = colors.GREEN
                self.message_text.update()
                return e.files
            else:
                self.text_selected_file.value = 'Chybný formát súboru!'
                self.text_selected_file.bgcolor = colors.RED
                self.text_selected_file.update()
                self.message_text.value = 'Načítať môžeš iba XLSX súbor!'
                self.message_text.color = colors.RED
                self.message_text.update()
                return None
        else:
            self.text_selected_file.value = 'Zrušené!'
            self.text_selected_file.bgcolor = colors.RED
            self.text_selected_file.update()
            self.message_text.value = 'Súbor nebol načítaný!'
            self.message_text.color = colors.RED
            self.message_text.update()
            return None

    def pick_path_result(self, e: ft.FilePickerResultEvent):
        if e.path is not None:
            self.text_selected_path.value = e.path
            self.text_selected_path.update()
            self.message_text.value = 'Adresár úspešne načítaný!'
            self.message_text.color = colors.GREEN
            self.message_text.update()
            return e.path
        else:
            self.text_selected_path.value = 'Zrušené!'
            self.text_selected_path.bgcolor = colors.RED
            self.text_selected_path.update()
            self.message_text.value = 'Adresár nebol načítaný!'
            self.message_text.color = colors.RED
            self.message_text.update()
            return None

    def draw_output(self):
        for path in self.cleared_path_list:
            self.output_text.controls.append(
                ft.Container(
                    content=ft.Text(
                        value=path,
                        color=colors.BLACK
                    )
                )
            )
            self.label_output_text.value = 'Vytvorene adresare'
            self.label_output_text.update()
            self.output_text.update()

    def generate_folders(self, e):
        if self.dialog_pick_file.result.files is None or self.dialog_select_path.result.path is None:
            self.message_text.value = "Zle vyplnený formulár!"
            self.message_text.color = colors.RED
            self.message_text.update()
        else:
            self.message_text.value = 'Spracovávam údaje!'
            self.message_text.color = colors.GREEN
            self.message_text.update()

            files = self.dialog_pick_file.result.files
            selected_path = self.dialog_select_path.result.path
            excel_file = load_excel_file(files[0].path, self.value_sheet_name_input.value)
            get_files_from_excel(excel_file)
            path_list = generate_path_list(excel_file)
            self.cleared_path_list = folder_generator(files[0].path, selected_path, path_list)
            save_path_to_db(self.cleared_path_list)
            self.draw_output()
            self.message_text.value = 'Údaje spracované!'
            self.message_text.color = colors.GREEN
            self.message_text.update()
