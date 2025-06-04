import flet as ft
from typing import Callable, Any
from components.history import HistoryItem
from core.color_utils import get_complementary_color

class UserPaletteColorDisplay(ft.Column):
    def __init__(self, palette: list, remove_color: Callable, change_bg: Callable, text_click: Callable, **kwargs):
        self.palette = palette
        self.remove_color = remove_color
        self.change_bg = change_bg
        self.text_click = text_click
        super().__init__(
            controls=self._build_controls(),
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=75,
            spacing=0,
            **kwargs,
        )

    def _build_controls(self):
        controls = []
        for color in self.palette:
            controls.append(
                UserPaletteItem(
                    color=color,
                    remove_color=self.remove_color,
                    change_bg=self.change_bg,
                    text_click=self.text_click
                )
            )
        return controls

    def update_palette(self, palette):
        self.palette = palette
        self.controls.clear()
        self.controls.extend(self._build_controls())

class UserPalette(ft.Row):
    def __init__(self, change_bg: Callable, comp_color: str, text_click: Callable[[ft.ControlEvent], None], **kwargs: Any):
        self.change_bg = change_bg
        self.text_click = text_click
        self.buttons_row = UserPaletteButtons(
            add_color=self._handle_add_color,
            remove_color=self._remove_color,
            initial_color=comp_color
        )
        self.palette = []
        self.palette_display = UserPaletteColorDisplay(
            palette=self.palette,
            remove_color=self._remove_color,
            change_bg=self.change_bg,
            text_click=self.text_click
        )
        super().__init__(
            controls=[self.buttons_row, self.palette_display],
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            **kwargs,
        )
        self.update_palette()

    def _get_palette(self, page=None):
        if page is None:
            page = getattr(self, 'page', None)
        if page and hasattr(page, 'session') and page.session is not None:
            palette = page.session.get('user_palette')
            if isinstance(palette, list):
                return palette
        return []

    def _set_palette(self, palette, page=None):
        if page is None:
            page = getattr(self, 'page', None)
        if page and hasattr(page, 'session') and page.session is not None:
            page.session.set('user_palette', palette)

    def _handle_add_color(self, e):
        page = e.page
        mixed = getattr(page, 'bgcolor', None)
        palette = self._get_palette(page)
        if mixed and mixed not in palette:
            palette.append(mixed)
            self._set_palette(palette, page)
            self.update_palette()
            self.palette_display.update_palette(palette)
            self.update()
            page.update()

    def _remove_color(self, e):
        page = e.page
        color = page.bgcolor
        palette = self._get_palette(page)
        if color in palette:
            palette.remove(color)
            self._set_palette(palette, page)
            self.update_palette()
            self.palette_display.update_palette(palette)
            self.update()
            page.update()

    def update_palette(self):
        page = getattr(self, 'page', None)
        palette = self._get_palette(page)
        if palette is not None and page and hasattr(page, 'session') and page.session is not None:
            page.session.set('user_palette', palette)
        bgcolor = getattr(page, 'bgcolor', None)
        if len(palette) != 0 and bgcolor in palette:
            self.buttons_row.show_remove_button()
        else:
            self.buttons_row.hide_remove_button()
        self.palette = palette
        self.palette_display.update_palette(palette)
        parent = getattr(self, 'parent', None)
        if len(palette) == 0:
            if self.palette_display in self.controls:
                self.controls.remove(self.palette_display)
            if isinstance(parent, ft.Row) and len(parent.controls) > 1 and isinstance(parent.controls[1], ft.Container):
                parent.controls[1].padding = ft.Padding(35, 0, 0, 0)
                parent.controls[1].update()
        else:
            if self.palette_display not in self.controls:
                self.controls.append(self.palette_display)
            if isinstance(parent, ft.Row) and len(parent.controls) > 1 and isinstance(parent.controls[1], ft.Container):
                parent.controls[1].padding = ft.Padding(110, 0, 0, 0)
                parent.controls[1].update()

    def update_button_color(self, color: str):
        self.buttons_row.update_button_color(color)

class UserPaletteItem(HistoryItem):
    def __init__(self, color: str, remove_color: Callable[[str], None], change_bg: Callable[[dict], None], text_click: Callable[[ft.ControlEvent], None], **kwargs: Any):
        super().__init__(
            item={'hex': color},
            change_bg=change_bg,
            text_click=text_click,
            rotate_text=False,
            alignment=ft.alignment.center,
            height=65,
            expand=True,
            **kwargs
        )
        self.on_click = self._handle_click
        self.color = color
        self.change_bg = change_bg

    def _handle_click(self, e: ft.ControlEvent):
        self.change_bg({'hex': self.color})

class UserPaletteButtons(ft.Column):
    def __init__(
        self,
        add_color: Callable[[ft.ControlEvent], None],
        remove_color: Callable[[ft.ControlEvent], None],
        initial_color: str
    ):
        self.add_color = add_color
        self.remove_color = remove_color
        self.remove_button = ft.IconButton(
            icon=ft.Icons.REMOVE_OUTLINED,
            padding=0,
            tooltip="Remove from palette",
            icon_color=initial_color,
            data="remove"
        )
        self.add_button = ft.IconButton(
            icon=ft.Icons.ADD_OUTLINED,
            padding=0,
            tooltip="Add to palette",
            icon_color=initial_color,
            data="add"
        )
        super().__init__(
            width=35,
            controls=[
                self.add_button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )
        self.add_button.on_click = self._handle_add_click
        self.remove_button.on_click = self._handle_remove_click

    def _handle_add_click(self, e):
        if callable(self.add_color):
            self.add_color(e)
        if self.remove_button not in self.controls and e.page.bgcolor in e.page.session.get('user_palette'):
            self.controls.append(self.remove_button)
        e.page.update()

    def _handle_remove_click(self, e):
        if callable(self.remove_color):
            self.remove_color(e)

    def update_button_color(self, color: str):
        self.add_button.icon_color = color
        self.remove_button.icon_color = color

    def show_remove_button(self):
        if self.remove_button not in self.controls:
            self.controls.append(self.remove_button)
        if self.add_button in self.controls:
            self.controls.remove(self.add_button)

    def hide_remove_button(self):
        if self.remove_button in self.controls:
            self.controls.remove(self.remove_button)
        if self.add_button not in self.controls:
            self.controls.append(self.add_button)
