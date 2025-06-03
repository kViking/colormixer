# Color Mixer Changelog

## [0.2.4] - 2025-06-03
### Added
- **User Palette:** You can now save your favorite colors to a personal palette column. Add any color with the + button, remove with the – button, and instantly recall any palette color with a click.
- **Click to Copy:** Click the color code label in your palette to copy it to your clipboard instantly.

### Changed
- The user palette column only appears when you have saved colors, keeping the interface clean when not in use.
- The input row's left padding now dynamically adjusts (110px with palette, 35px without) for a consistent, balanced layout.
- All user palette logic is now modularized in `components/user_palette.py` for easier maintenance and extension.

### Fixed
- No accidental palette clearing: clicking a palette color only changes the background, never deletes your palette.
- All debug print statements and explanation comments have been removed for production readiness.

---

## [0.2.3] - 2025-06-02
### Added
- Hotkey navigation for color exploration (arrow keys, shift-modified for fine/coarse steps).
- Clickable color swatch and color value labels for instant copy-to-clipboard.
- Windows installer script with version auto-bumping and user-friendly notifications.
- Modern, accessible UI with clear color contrast and helper labels.
- Comprehensive onboarding and hacking guides for users and developers.

### Changed
- Major UI refactor: clearer color display, consistent helper labels, and improved color contrast for readability.
- All color display labels now use bracketed, all-caps style (e.g., `[BACKGROUND]`, `[COMPLEMENTARY]`, `[RGB]`).
- Improved error handling and feedback for invalid color input.
- Color mixing and swatch logic is more robust and user-friendly.
- Faster, more reliable color updates and navigation.

### Fixed
- Fixed issues with color label updates and helper label color consistency.
- Fixed history and undo/redo logic for color changes.
- Fixed installer script bugs and improved build reliability.
- Fixed test coverage for all major UI and logic components.

### Removed
- Removed YAML config dependency; now uses a Python config for easier customization.
- Removed legacy and redundant code for a cleaner, faster app.

---

Thank you for using Color Mixer! If you have feedback or feature requests, please see the README or contact support.

## [0.1.6] - 2025-05-30

### Added

- **Type Annotations**: Comprehensive type annotations have been added throughout the codebase (see `main.py`, `components.py`). This improves static analysis, IDE support, and code safety ([PEP 484](https://peps.python.org/pep-0484/)).
- **Docstrings**: All public classes and functions now include detailed docstrings following [PEP 257](https://peps.python.org/pep-0257/), aiding maintainability and documentation generation.
- **Palette Restoration**: Swatch clicks and history items now support passing and restoring color palettes. This enables richer user experiences and more robust state management (see `ColorSwatch`, `HistoryItem` in `components.py`).
- **Route Parameter in SwatchRow**: The `SwatchRow` component now accepts an optional `route` parameter for future extensibility and navigation features.

### Changed

- **update_text_colors Refactor**: The `update_text_colors` function in `main.py` was refactored to ensure random color choices for UI elements never match the current background color. This improves visual clarity and user experience.
- **Error Handling**: All print/debug statements have been removed. Error handling is now more robust, with exceptions logged using `traceback.print_exc()` for easier debugging.
- **Pythonic Style**: The codebase was reviewed for Pythonic best practices ([PEP 8](https://peps.python.org/pep-0008/)), including improved naming, modularity, and code readability. Redundant assignments and comments were removed.
- **History Logic**: The logic for updating and displaying color history was updated to prevent duplicate or invalid entries. History entries are now always dictionaries with explicit keys (`hex`, `pair`, `colors`).

### Fixed

- **ColorSwatch Clicks**: Fixed a bug where clicking a `ColorSwatch` did not update the background or add to history. Now, swatch clicks reliably update the UI and persist the palette in history.
- **Palette Handling**: Resolved issues with palette handling and UI updates after swatch/history actions. The palette is now always a non-empty list of valid hex color strings.
- **Color Normalization**: Corrected potential errors in color normalization and palette updates, especially when handling invalid or missing color values.
- **Type Safety**: Addressed all outstanding type warnings, including float/int mismatches and optional value handling, to ensure runtime and static safety.

### References & Annotations

- **Type Annotations**: [PEP 484](https://peps.python.org/pep-0484/), [PEP 526](https://peps.python.org/pep-0526/)
- **Docstrings**: [PEP 257](https://peps.python.org/pep-0257/)
- **Python Style Guide**: [PEP 8](https://peps.python.org/pep-0008/)
- **Error Handling**: [traceback — Print or retrieve a stack traceback](https://docs.python.org/3/library/traceback.html)
- **Flet UI Library**: [Flet Documentation](https://flet.dev/docs/)

### File Annotations

- `main.py`: Main application logic, color mixing, UI orchestration, history management, and type safety improvements.
- `components.py`: UI component classes (`ColorInput`, `MixedColorText`, `MixedRGBText`, `ComplementaryColorText`, `RandomFAB`, `InputRow`, `SwatchRow`, `ColorSwatch`, `HistoryRow`, `HistoryItem`) with updated history handling, palette support, and robust typing.
- `swatches.json`: Color swatch data used for palette and swatch row features.

---
