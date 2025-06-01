import flet as ft
from typing import Callable, List, Dict, Any, Optional
from color_utils import get_complementary_color, CloseSwatch

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
        self._match: Optional[CloseSwatch] = None

    def update_swatch_row(self, match: CloseSwatch, page: ft.Page, make_bottom_sheet: Callable, route: Optional[str] = None) -> None:
        self.controls.clear()
        self._page = page
        self._make_bottom_sheet = make_bottom_sheet
        self._match = match
        self._route = route
        bgcolor = page.bgcolor if isinstance(page.bgcolor, str) and page.bgcolor else "#000000"
        combinations = match.get('combinations') or []
        for combo in combinations:
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
        combo_row = ft.Row(expand=True, alignment=ft.MainAxisAlignment.CENTER, spacing=0)
        sheet = ft.BottomSheet(
            ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
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
                        on_click=text_click,
                    )
                )
        return sheet

class ColorSwatch(ft.Container):
    """Change the background color and palette when clicked."""
    def __init__(self, color: str, name: str, change_bg: Callable[[Dict[str, Any]], None], on_click: Callable, palette: List[str], **kwargs: Any):
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
        self.alignment = ft.alignment.top_left
        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
            controls=[
            ft.Text(
                theme_style=ft.TextThemeStyle.BODY_LARGE,
                text_align=ft.TextAlign.RIGHT,
                expand=True,
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
        self.change_bg({"hex": self.color, "colors": self.palette})

class SwatchRowContainer(ft.Container):
    """A container for SwatchRow, for flexible layout and styling."""
    def __init__(self, **kwargs: Any):
        self.swatch_row = SwatchRow()
        super().__init__(
            content=self.swatch_row,
            **kwargs,
        )
