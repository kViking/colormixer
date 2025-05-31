import flet as ft
from typing import Callable, List, Dict, Any, Optional
import math
from color_utils import get_complementary_color, hex_to_rgb


class ColorInput(ft.TextField):
    """Create a text input field for color values."""
    def __init__(self, on_change: Callable, on_submit: Callable, **kwargs: Any):
        super().__init__(
            on_submit=on_submit,
            on_change=on_change,
            text_align=ft.TextAlign.CENTER,
            border_radius=ft.BorderRadius(0,0,0,0),
            width=200,
            **kwargs,
        )

    def update_color(self, color: str) -> None:
        self.color = color
        

    def update_bg_color(self, color: str) -> None:
        self.bgcolor = color
        

    def update_focused_border_color(self, color: str) -> None:
        self.focused_border_color = color

    def update_border_color(self, color: str) -> None:
        self.border_color = color
        


class MixedColorText(ft.Text):
    """Display the mixed color hex value, clickable for copy."""
    def __init__(self, initial_bg: str, on_click: Callable, **kwargs: Any):
        super().__init__(
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
            spans=[ft.TextSpan(initial_bg, on_click=on_click)],
            **kwargs,
        )

    def update_color(self, color: str) -> None:
        self.spans[0].style = ft.TextStyle(color=color)
        


class ComplementaryColorText(ft.Text):
    """Display the complementary color, clickable for copy."""
    def __init__(self, complementary_color: str, on_click: Callable, **kwargs: Any):
        super().__init__(
            theme_style=ft.TextThemeStyle.DISPLAY_SMALL,
            spans=[
                ft.TextSpan(
                    complementary_color,
                    on_click=on_click,
                    style=ft.TextStyle(color=complementary_color),
                )
            ],
            **kwargs,
        )

    def update_color(self, new_color: str) -> None:
        self.spans[0].style = ft.TextStyle(color=new_color)
        


class MixedRGBText(ft.Text):
    """Display the mixed color as an RGB tuple, clickable for copy."""
    def __init__(self, initial_bg: str, on_click: Callable, **kwargs: Any):
        rgb_str = hex_to_rgb(initial_bg)

        super().__init__(
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
            selectable=True,
            spans=[ft.TextSpan(text=rgb_str, on_click=on_click, style=ft.TextStyle(color=get_complementary_color(initial_bg)))],
            **kwargs,
        )
        print(f"MixedRGBText initialized with initial_bg: {initial_bg}, rgb_str: {rgb_str}")
        print(f"Comp: {get_complementary_color(initial_bg)}")

    def update_color(self, color) -> None:
        self.spans[0].style = ft.TextStyle(color=color)


class RandomFAB(ft.FloatingActionButton):
    """Randomize the background color and update history."""
    def __init__(
        self, page: ft.Page, mixed_color: MixedColorText, mixed_rgb: MixedRGBText, color1: ColorInput, color2: ColorInput,
        update_text_colors: Callable, history: List[Dict[str, Any]], history_row: 'HistoryRow', **kwargs: Any
    ):
        super().__init__(
            icon=ft.Icons.SHUFFLE,
            on_click=self._handle_click,
            tooltip="Randomize background color",
            **kwargs,
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

    def update_color(self, color: str) -> None:
        self.bgcolor = color
        if hasattr(self, 'page') and self.page is not None and hasattr(self.page, 'bgcolor') and isinstance(self.page.bgcolor, str):
            self.foreground_color = self.page.bgcolor
        else:
            self.foreground_color = get_complementary_color(color)
        

    def _handle_click(self, e: ft.ControlEvent) -> None:
        """Randomize color, update UI, and add to history."""
        import random
        new_color = f"#{random.randint(0, 0xFFFFFF):06x}"
        if self.page is not None:
            self.page.bgcolor = new_color

        try:
            self.mixed_color.spans[0].text = new_color
            self.mixed_rgb.spans[0].text = hex_to_rgb(new_color)
        except (AttributeError, IndexError):
            pass

        for field in (self.color1, self.color2):
            field.value = ""

        if not self.history or self.history[-1] != new_color:
            self.history.append({'hex': new_color})
            self.history_row.update_history(self.history)

        self.update_text_colors(bg_color=new_color)
        if self.page is not None:
            self.page.update()


class InputRow(ft.Row):
    """Create a row containing the two color input fields."""
    def __init__(self, color1: ColorInput, color2: ColorInput, **kwargs: Any):
        super().__init__(
            controls=[color1, color2],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            wrap=True,
            **kwargs,
        )
        


class SwatchRow(ft.Row):
    """Display color swatch combinations and handle swatch selection."""
    def __init__(self, **kwargs: Any):
        super().__init__(
            alignment=ft.MainAxisAlignment.START,
            controls=[],
            **kwargs,
        )
        self.height = 18
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self._page: Optional[ft.Page] = None
        self._make_bottom_sheet: Optional[Callable] = None
        self._match: Optional[Dict[str, Any]] = None

    def update_swatch_row(self, match: Optional[Dict[str, Any]], page: ft.Page, make_bottom_sheet: Callable, route: Optional[str] = None) -> None:
        """Update the swatch row with new swatch combinations."""
        self.controls.clear()
        self._page = page
        self._make_bottom_sheet = make_bottom_sheet
        self._match = match
        self._route = route
        bgcolor = page.bgcolor if isinstance(page.bgcolor, str) and page.bgcolor else "#000000"
        if match:
            for combo in match['combinations']:
                self.controls.append(
                    ft.Text(
                        theme_style=ft.TextThemeStyle.BODY_LARGE,
                        spans=[
                            ft.TextSpan(
                                combo,
                                style=ft.TextStyle(color=get_complementary_color(bgcolor)),
                                on_click=self._handle_combo_click,
                            )
                        ],
                    )
                )
        page.update()

    def _handle_combo_click(self, e: ft.ControlEvent) -> None:
        """Open the bottom sheet for the selected combo."""
        combo = e.control.text
        if self._page is not None and self._make_bottom_sheet is not None:
            self._page.open(self._make_bottom_sheet(combo, self._match))

    def make_bottom_sheet(
        self,
        combination: str,
        match: Dict[str, Any],
        swatches: List[Dict[str, Any]],
        change_bg: Callable[[Dict[str, str]], None],
    ) -> ft.BottomSheet:
        """Create and return a bottom sheet UI for a swatch combination."""
        combo_row = ft.Row(expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=0)
        sheet = ft.BottomSheet(
            ft.Column(
                controls=[
                    combo_row,
                    ft.Text(
                        f"combination {combination}",
                        style=ft.TextStyle(color=get_complementary_color(match['hex'])),
                    ),
                ],
                expand=True,
            ),
            bgcolor=match['hex'],
        )
        for swatch in swatches:
            if combination in swatch['combinations']:
                color = swatch['hex']
                name = swatch['name']
                palette = [x['hex'] for x in swatches if combination in x['combinations']]
                combo_row.controls.append(
                    ColorSwatch(
                        color,
                        name,
                        change_bg=change_bg,
                        palette=palette,
                    )
                )
        return sheet


class ColorSwatch(ft.Container):
    """Change the background color and palette when clicked."""
    def __init__(self, color: str, name: str, change_bg: Callable[[Dict[str, Any]], None], palette: List[str], **kwargs: Any):
        super().__init__(
            bgcolor=color,
            expand=True,
            alignment=ft.alignment.center,
            **kwargs,
        )
        self.palette = palette
        self.color = color
        self.name = name
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
                            style=ft.TextStyle(color=get_complementary_color(color)),
                        )
                    ],
                    expand=True,
                ),
                ft.Text(
                    name,
                    color=get_complementary_color(color),
                    theme_style=ft.TextThemeStyle.BODY_LARGE,
                ),
            ],
        )

    def _handle_click(self, e: ft.ControlEvent) -> None:
        """Change the background color and palette to this swatch's color."""
        self.change_bg({"hex": self.color, "colors": self.palette})


class HistoryRow(ft.Row):
    """Display the color mixing history as clickable items."""
    def __init__(self, history: List[Dict[str, Any]], change_bg: Callable, **kwargs: Any):
        super().__init__(
            controls=[
                HistoryItem(
                    item,
                    change_bg=change_bg,
                )
                for item in history
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
            **kwargs,
        )
        self.history = history[::-1]
        self.change_bg = change_bg

    def update_history(self, history: List[Dict[str, Any]]) -> None:
        """Update the history row with new history entries."""
        self.controls.clear()
        history = history[::-1]
        for item in history:
            self.controls.append(
                HistoryItem(item, self.change_bg)
            )


class HistoryItem(ft.Container):
    """Restore a previously selected color when clicked."""
    def __init__(self, item: Dict[str, Any], change_bg: Callable, **kwargs: Any):
        super().__init__(**kwargs)
        self.item = item
        hex_color = item['hex'] if isinstance(item, dict) and 'hex' in item else str(item)
        self.complementary_color = get_complementary_color(hex_color)
        self.on_click = lambda e: change_bg(self.item, clear_fields=True)
        self.bgcolor = hex_color
        self.alignment = ft.alignment.center
        text_value = hex_color
        self.content = ft.Text(
            value=text_value,
            text_align=ft.TextAlign.CENTER,
            color=self.complementary_color,
            height=65,
            width=65,
            rotate=ft.Rotate(angle=math.pi / 2),
        )