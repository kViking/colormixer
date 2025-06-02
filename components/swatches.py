import flet as ft
from typing import Callable, List, Dict, Any, Optional
from core.color_utils import get_complementary_color, CloseSwatch

class CombinationRow(ft.Row):
    """Display color combination swatches and handle combination selection."""
    def __init__(self, **kwargs: Any):
        super().__init__(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[],
            **kwargs,
        )
        self.height = 18
        self._page: Optional[ft.Page] = None
        self._make_bottom_sheet: Optional[Callable] = None
        self._match: Optional[CloseSwatch] = None

    def update_combination_row(self, match: CloseSwatch, page: ft.Page, make_bottom_sheet: Callable, route: Optional[str] = None) -> None:
        self.controls.clear()
        self._page = page
        self._make_bottom_sheet = make_bottom_sheet
        self._match = match
        self._route = route
        bgcolor = getattr(page, "bgcolor", None)
        current_state = page.session.get('current')
        if isinstance(current_state, dict):
            if not (isinstance(bgcolor, str) and bgcolor):
                bgcolor = current_state.get('bgcolor')
            palette = current_state.get('palette_colors')
            if current_state.get('palette'):
                current_combo = current_state.get('palette')
        if not (isinstance(bgcolor, str) and bgcolor):
            raise ValueError("No valid background color in UI or session state.")
        combinations = match.get('combinations') or []
        for combo in combinations:
            # Only set the default style, do not attempt to highlight or select here
            style = ft.TextStyle(
                color=get_complementary_color(bgcolor),
                bgcolor=None,
            )
            self.controls.append(
                ft.Text(
                    theme_style=ft.TextThemeStyle.BODY_LARGE,
                    spans=[
                        ft.TextSpan(
                            combo,
                            style=style,
                            on_click=self._handle_combo_click,
                        )
                    ],
                )
            )
        page.update()

    def _handle_combo_click(self, e: ft.ControlEvent) -> None:
        combo = e.control.text
        if self._page is not None and self._make_bottom_sheet is not None:
            self._page.open(self._make_bottom_sheet(combo, self._match))

    def make_bottom_sheet(
        self,
        combination: str,
        match: Dict[str, Any],
        swatches: List[Dict[str, Any]],
        change_bg: Callable[[Dict[str, str]], None],
        text_click: Callable[[ft.ControlEvent], None],
    ) -> ft.BottomSheet:
        combo_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=0, expand=True)
        sheet = ft.BottomSheet(
            ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    combo_row,
                    ft.Text(
                        f"combination {combination}",
                        style=ft.TextStyle(color=get_complementary_color(match['hex'])),
                    ),
                ],
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
                        on_click=text_click,
                        combination=combination,
                    )
                )
        return sheet

class ColorSwatch(ft.Container):
    """Change the background color and palette when clicked."""
    def __init__(self, color: str, name: str, change_bg: Callable[[Dict[str, Any]], None], on_click: Callable, palette: List[str], combination: str, **kwargs: Any):
        super().__init__(
            bgcolor=color,
            alignment=ft.alignment.center,
            **kwargs,
        )
        self.palette = palette
        self.combination = combination
        self.color = color
        self.name = name
        self.expand = kwargs.pop('expand', True)
        self.change_bg = change_bg
        self.on_click = self._handle_click
        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    theme_style=ft.TextThemeStyle.BODY_LARGE,
                    text_align=ft.TextAlign.RIGHT,
                    spans=[
                        ft.TextSpan(
                            color,
                            style=ft.TextStyle(color=get_complementary_color(color)),
                            on_click=on_click
                        )
                    ],
                ),
                ft.Text(
                    name,
                    color=get_complementary_color(color),
                    theme_style=ft.TextThemeStyle.BODY_LARGE,
                ),
            ],
        )
    def _handle_click(self, e: ft.ControlEvent) -> None:
        # Pass the combination number and palette colors
        self.change_bg({"hex": self.color, "palette": self.combination, "palette_colors": self.palette})

class CombinationRowContainer(ft.Container):
    """A container for CombinationRow, for flexible layout and styling."""
    def __init__(self, **kwargs: Any):
        self.combination_row = CombinationRow()
        super().__init__(
            content=self.combination_row,
            **kwargs,
        )
