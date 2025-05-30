import flet as ft

class ColorInput(ft.TextField):
    def __init__(self, on_change, on_submit, **kwargs):
        super().__init__(
            on_submit=on_submit,
            on_change=on_change,
            text_align=ft.TextAlign.CENTER,
            width=200,
            **kwargs
        )

class MixedColorText(ft.Text):
    def __init__(self, initial_bg, on_click, **kwargs):
        super().__init__(
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
            spans=[ft.TextSpan(initial_bg, on_click=on_click)],
            **kwargs
        )


class ComplementaryColorText(ft.Text):
    def __init__(self, complementary_color, on_click, **kwargs):
        super().__init__(
            theme_style=ft.TextThemeStyle.DISPLAY_SMALL,
            spans=[ft.TextSpan(
                complementary_color, 
                on_click=on_click,
                style=ft.TextStyle(color=complementary_color)
            )],
            **kwargs
        )

    def update_color(self, new_color):
        self.spans[0].text = new_color
        self.spans[0].style = ft.TextStyle(color=new_color)

class MixedRGBText(ft.Text):
    def __init__(self, initial_bg, on_click, **kwargs):
        rgb_str = tuple(int(initial_bg[i:i+2], 16) for i in (1, 3, 5)).__str__()
        super().__init__(
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
            selectable=True,
            spans=[ft.TextSpan(rgb_str, on_click=on_click)],
            **kwargs
        )

class RandomFAB(ft.FloatingActionButton):
    def __init__(self, page, mixed_color, mixed_rgb, color1, color2, update_text_colors, history, history_row, **kwargs):
        super().__init__(
            icon=ft.Icons.SHUFFLE,
            on_click=self._handle_click,
            tooltip="Randomize background color",
            **kwargs
        )
        self.page = page
        self.mixed_color = mixed_color
        self.mixed_rgb = mixed_rgb
        self.color1 = color1
        self.color2 = color2
        self.update_text_colors = update_text_colors
        self.history = history
        self.history_row = history_row
        self.on_click = self._handle_click

    def _handle_click(self, e):
        import random
        new_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        if self.page is not None:
            self.page.bgcolor = new_color

        # Update color displays
        try:
            self.mixed_color.spans[0].text = new_color
            self.mixed_rgb.spans[0].text = str(tuple(int(new_color[i:i+2], 16) for i in (1, 3, 5)))
        except (AttributeError, IndexError):
            pass

        # Clear input fields
        for field in (self.color1, self.color2):
            field.value = ""

        # Add to history if not duplicate
        if len(self.history) == 0 or self.history[-1] != new_color:
            self.history.append({'hex': new_color})
            self.history_row.update_history(self.history)

        # Update text colors and page
        self.update_text_colors(new_color)
        if self.page is not None:
            self.page.update()

class InputRow(ft.Row):
    def __init__(self, color1, color2, **kwargs):
        super().__init__(
            controls=[color1, color2],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            wrap=True,
            **kwargs
        )

class SwatchRow(ft.Row):
    def __init__(self, get_complementary_color, **kwargs):
        super().__init__(
            alignment=ft.MainAxisAlignment.START,
            controls=[],
            **kwargs
        )
        self.height = 18
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self._page = None
        self._make_bottom_sheet = None
        self._match = None
        self.get_complementary_color = get_complementary_color

    def update_swatch_row(self, match, page, make_bottom_sheet):
        self.controls.clear()
        self._page = page
        self._make_bottom_sheet = make_bottom_sheet
        self._match = match
        if match:
            for combo in match['combinations']:
                self.controls.append(
                    ft.Text(
                        theme_style=ft.TextThemeStyle.BODY_LARGE,
                        spans=[
                            ft.TextSpan(
                                combo,
                                style=ft.TextStyle(color=self.get_complementary_color(page.bgcolor)),
                                on_click=self._handle_combo_click,
                            )
                        ]
                    )
                )
        page.update()

    def _handle_combo_click(self, e):
        combo = e.control.text
        if self._page is not None and self._make_bottom_sheet is not None:
            self._page.open(self._make_bottom_sheet(combo, self._match))

    def make_bottom_sheet(self, combination, match, swatches, get_complementary_color, change_bg):
        combo_row = ft.Row(expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=0)
        sheet = ft.BottomSheet(
            ft.Column(
                controls=[
                    combo_row,
                    ft.Text(f"combination {combination}", style=ft.TextStyle(color=get_complementary_color(match['hex'])))
                ],
                expand=True,
            ),
            bgcolor=match['hex'],
        )
        for swatch in swatches:
            if combination in swatch['combinations']:
                color = swatch['hex']
                name = swatch['name']
                combo_row.controls.append(ColorSwatch(color, name, get_complementary_color=get_complementary_color, change_bg=change_bg))
        return sheet

class ColorSwatch(ft.Container):
    def __init__(self, color, name, get_complementary_color, change_bg, **kwargs):
        super().__init__(
            bgcolor=color,
            expand=True,
            alignment=ft.alignment.center,
            **kwargs
        )
        self.color = color
        self.name = name
        self.get_complementary_color = get_complementary_color
        self.change_bg = change_bg
        self.on_click = self._handle_click
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.END,
            expand=True,
            controls=[
                ft.Text(
                    theme_style=ft.TextThemeStyle.BODY_LARGE,
                    spans=[
                        ft.TextSpan(
                            color,
                            style=ft.TextStyle(color=self.get_complementary_color(color))
                        )
                    ],
                    expand=True
                ),
                ft.Text(
                    name, 
                    color=self.get_complementary_color(color),
                    theme_style=ft.TextThemeStyle.BODY_LARGE,
                ),
            ],
        )

    def _handle_click(self, e):
        # Always call with a dict so change_bg adds to history
        self.change_bg({"hex": self.color})

class HistoryRow(ft.Row):
    def __init__(self, history, get_complementary_color, change_bg, **kwargs):
        super().__init__(
            controls=[
                HistoryItem(
                    item, 
                    get_complementary_color=get_complementary_color, 
                    change_bg=change_bg
                ) for item in history
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
            **kwargs,
        )

        self.history = history[::-1]
        self.get_complementary_color = get_complementary_color
        self.change_bg = change_bg

    def update_history(self, history):
        self.controls.clear()
        history = history[::-1]  # Reverse the history for display
        for item in history:
            self.controls.append(
                HistoryItem(item, self.get_complementary_color, self.change_bg)
            )

class HistoryItem(ft.Container):
    def __init__(self, item, get_complementary_color, change_bg, **kwargs):
        super().__init__(**kwargs)
        self.item = item
        # Expect item to be a dict with 'hex' and optional 'pair'
        hex_color = item['hex'] if isinstance(item, dict) and 'hex' in item else str(item)
        self.complementary_color = get_complementary_color(hex_color)
        self.on_click = lambda e: change_bg(self.item, clear_fields=True)
        self.bgcolor = hex_color
        self.alignment = ft.alignment.bottom_left
        # Only show hex, do not display pair
        text_value = hex_color
        self.content = ft.Text(
            value=text_value,
            text_align=ft.TextAlign.CENTER,
            color=self.complementary_color,
            height=65,
            width=65,
            rotate=ft.Rotate(angle=3.14159/2)  # π/2 radians = 90 degrees
        )