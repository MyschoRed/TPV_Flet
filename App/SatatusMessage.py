import flet as ft
from flet import colors


class StatusMessage:
    def __init__(self):
        super().__init__()
        self.message = ft.Text(
            color=colors.BLACK,
            size=15)
        self.msg_section = ft.Row(
            controls=[
                self.message
            ]
        )

    def write_msg(self, msg_type, msg_text):
        if msg_type == 'error':
            self.message.value = msg_text
            self.message.color = colors.RED
        elif msg_type == 'info':
            self.message.value = msg_text
            self.message.color = colors.BLUE
        elif msg_type == 'success':
            self.message.value = msg_text
            self.message.color = colors.GREEN
        print(self.message)
        return self.message
