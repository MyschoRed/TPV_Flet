from flet import Row, Page, Container, colors, Column


class AppLayout(Row):
    def __init__(self, app, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.detail_frame = Container(content=Row(),
                                      width=1200 / 3,
                                      height=800 - 170,
                                      bgcolor=colors.WHITE,
                                      border_radius=10)

        self.main_frame = Container(content=Row(),
                                    width=1200 / 1.556,
                                    # width=120,
                                    height=800 - 170,
                                    # height=170,
                                    bgcolor=colors.WHITE,
                                    border_radius=10)

        self.status_bar = Container(content=Row(),
                                    width=1180,
                                    height=45,
                                    padding=12,
                                    bgcolor=colors.WHITE,
                                    border_radius=10)

        self.main_section = Row(controls=[self.detail_frame, self.main_frame])
        self.frame = Column(controls=[self.main_section, self.status_bar])
        self.controls = [self.frame]
