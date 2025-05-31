# Changelog

## [Unreleased] - 2025-05-31

### Customer-Facing Changes

- **Clickable Swatch Labels:**
  - You can now click on the color label text in each swatch (the color hex code) to trigger actions, thanks to the new `TextSpan.on_click` method in the ColorSwatch component. This makes it easier to interact with and copy color codes directly from the swatch display.

---

### Developer-Facing Changes

- **Component Refactoring & Modularization:**
  - All UI components have been modularized into the `components/` package for maintainability and clarity.
  - Each component (inputs, display, swatches, fab, history) is now in its own file with clear class boundaries and docstrings.

- **Type Safety & TypedDicts:**
  - The `find_closest_swatch` function now always returns a value matching the `CloseSwatch` TypedDict, ensuring type safety and consistency across the codebase.
  - All consuming code (e.g., `SwatchRow.update_swatch_row`) expects and handles this structure.

- **Event Handling & UI Logic:**
  - Event handler structure has been refactored for maintainability and clarity.
  - Hotkey navigation and color plane movement logic have been improved and debugged.
  - Focus tracking for Flet text fields is now robust and extensible.

- **Testing Infrastructure:**
  - Comprehensive test suite added under `tests/` covering color logic, state/history, UI components, and hotkey handling.
  - Dummy classes are used in tests to avoid Flet type errors and allow for isolated logic testing.

- **Installer & Build Improvements:**
  - Inno Setup script and build scripts have been updated for better version bumping and release automation.

- **Documentation:**
  - All public classes and functions now include detailed docstrings.
  - A markdown hacking guide (`1337.md`) and improved README for easier onboarding and customization.

- **General Code Quality:**
  - Improved error handling and guard clauses throughout.
  - Variable and function names are now concise but descriptive.
  - Redundant code and debug prints have been removed.

---

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
