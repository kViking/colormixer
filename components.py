import flet as ft
from typing import Callable, List, Dict, Any, Optional
import math


class ColorInput(ft.TextField):
    """A text input field for color values, with custom on_change and on_submit handlers."""
    def __init__(self, on_change: Callable, on_submit: Callable, **kwargs: Any):
        super().__init__(
            on_submit=on_submit,
            on_change=on_change,
            text_align=ft.TextAlign.CENTER,
            width=200,
            **kwargs,
        )


class MixedColorText(ft.Text):
    """A text widget displaying the mixed color hex value, clickable for copy."""
    def __init__(self, initial_bg: str, on_click: Callable, **kwargs: Any):
        super().__init__(
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
            spans=[ft.TextSpan(initial_bg, on_click=on_click)],
            **kwargs,
        )


class ComplementaryColorText(ft.Text):
    """A text widget displaying the complementary color, clickable for copy."""
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
        """Update the displayed complementary color."""
        self.spans[0].text = new_color
        self.spans[0].style = ft.TextStyle(color=new_color)


class MixedRGBText(ft.Text):
    """A text widget displaying the mixed color as an RGB tuple, clickable for copy."""
    def __init__(self, initial_bg: str, on_click: Callable, **kwargs: Any):
        rgb_str = str(tuple(int(initial_bg[i:i+2], 16) for i in (1, 3, 5)))
        super().__init__(
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
            selectable=True,
            spans=[ft.TextSpan(rgb_str, on_click=on_click)],
            **kwargs,
        )


class RandomFAB(ft.FloatingActionButton):
    """A floating action button that randomizes the background color and updates history."""
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

    def _handle_click(self, e: ft.ControlEvent) -> None:
        """Handle click event to randomize color, update UI, and add to history."""
        import random
        new_color = f"#{random.randint(0, 0xFFFFFF):06x}"
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
        if not self.history or self.history[-1] != new_color:
            self.history.append({'hex': new_color})
            self.history_row.update_history(self.history)

        # Update text colors and page
        self.update_text_colors(new_color)
        if self.page is not None:
            self.page.update()


class InputRow(ft.Row):
    """A row containing the two color input fields."""
    def __init__(self, color1: ColorInput, color2: ColorInput, **kwargs: Any):
        super().__init__(
            controls=[color1, color2],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            wrap=True,
            **kwargs,
        )


class SwatchRow(ft.Row):
    """A row displaying color swatch combinations and handling swatch selection."""
    def __init__(self, get_complementary_color: Callable[[str], str], **kwargs: Any):
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
        self.get_complementary_color = get_complementary_color

    def update_swatch_row(self, match: Optional[Dict[str, Any]], page: ft.Page, make_bottom_sheet: Callable, route: Optional[str] = None) -> None:
        """Update the swatch row with new swatch combinations. Optionally accepts a route."""
        self.controls.clear()
        self._page = page
        self._make_bottom_sheet = make_bottom_sheet
        self._match = match
        self._route = route  # Store the route if needed for future use
        bgcolor = page.bgcolor if isinstance(page.bgcolor, str) and page.bgcolor else "#000000"
        if match:
            for combo in match['combinations']:
                self.controls.append(
                    ft.Text(
                        theme_style=ft.TextThemeStyle.BODY_LARGE,
                        spans=[
                            ft.TextSpan(
                                combo,
                                style=ft.TextStyle(color=self.get_complementary_color(bgcolor)),
                                on_click=self._handle_combo_click,
                            )
                        ],
                    )
                )
        page.update()

    def _handle_combo_click(self, e: ft.ControlEvent) -> None:
        """Handle click event on a swatch combination."""
        combo = e.control.text
        if self._page is not None and self._make_bottom_sheet is not None:
            self._page.open(self._make_bottom_sheet(combo, self._match))

    def make_bottom_sheet(
        self,
        combination: str,
        match: Dict[str, Any],
        swatches: List[Dict[str, Any]],
        get_complementary_color: Callable[[str], str],
        change_bg: Callable[[Dict[str, str]], None],
    ) -> ft.BottomSheet:
        """Create a bottom sheet UI for a swatch combination."""
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
                combo_row.controls.append(
                    ColorSwatch(
                        color,
                        name,
                        get_complementary_color=get_complementary_color,
                        change_bg=change_bg,
                    )
                )
        return sheet


class ColorSwatch(ft.Container):
    """A clickable color swatch that changes the background color when clicked."""
    def __init__(self, color: str, name: str, get_complementary_color: Callable[[str], str], change_bg: Callable[[Dict[str, str]], None], **kwargs: Any):
        super().__init__(
            bgcolor=color,
            expand=True,
            alignment=ft.alignment.center,
            **kwargs,
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
                            style=ft.TextStyle(color=self.get_complementary_color(color)),
                        )
                    ],
                    expand=True,
                ),
                ft.Text(
                    name,
                    color=self.get_complementary_color(color),
                    theme_style=ft.TextThemeStyle.BODY_LARGE,
                ),
            ],
        )

    def _handle_click(self, e: ft.ControlEvent) -> None:
        """Handle click event to change the background color to this swatch's color."""
        # Always call with a dict so change_bg adds to history
        self.change_bg({"hex": self.color})


class HistoryRow(ft.Row):
    """A row displaying the color mixing history as clickable items."""
    def __init__(self, history: List[Dict[str, Any]], get_complementary_color: Callable[[str], str], change_bg: Callable, **kwargs: Any):
        super().__init__(
            controls=[
                HistoryItem(
                    item,
                    get_complementary_color=get_complementary_color,
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
        self.get_complementary_color = get_complementary_color
        self.change_bg = change_bg

    def update_history(self, history: List[Dict[str, Any]]) -> None:
        """Update the history row with new history entries."""
        self.controls.clear()
        history = history[::-1]  # Reverse the history for display
        for item in history:
            self.controls.append(
                HistoryItem(item, self.get_complementary_color, self.change_bg)
            )


class HistoryItem(ft.Container):
    """A clickable history item representing a previously selected color."""
    def __init__(self, item: Dict[str, Any], get_complementary_color: Callable[[str], str], change_bg: Callable, **kwargs: Any):
        super().__init__(**kwargs)
        self.item = item
        hex_color = item['hex'] if isinstance(item, dict) and 'hex' in item else str(item)
        self.complementary_color = get_complementary_color(hex_color)
        self.on_click = lambda e: change_bg(self.item, clear_fields=True)
        self.bgcolor = hex_color
        self.alignment = ft.alignment.bottom_left
        text_value = hex_color
        self.content = ft.Text(
            value=text_value,
            text_align=ft.TextAlign.CENTER,
            color=self.complementary_color,
            height=65,
            width=65,
            rotate=ft.Rotate(angle=math.pi / 2),  # π/2 radians = 90 degrees
        )