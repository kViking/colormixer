# 🎨 ColorMixer

ColorMixer lets you blend, explore, and copy colors with a clean, fast, and cross-platform interface. Whether you're a designer, developer, or just love color, this app is for you.

## Features

- **Mix Colors Instantly:** Enter two colors in any format (hex, RGB, with or without #, spaces or commas) and see the result.
- **Clickable Swatch Labels:** Click the color code in any swatch to copy or trigger actions—no more fiddling to grab a hex code.
- **Palette Exploration:** Instantly see and navigate color combinations and swatches.
- **Hotkey Navigation:** Use arrows (←/→/↑/↓) to explore the RGB color space without leaving your keyboard.
- **Cross-Platform:** Works on Linux, Windows, and Android. (Mac support coming soon!)
- **Minimalist UI:** No clutter, just color. Designed for speed and clarity.
- **History:** Quickly restore previous mixes and palettes.

## How to Use

1. **Open the app.**
2. **Enter two colors** in the input fields at the top. You can use any format: `#4edec1`, `4edec1`, `78, 90, 123`, `(78,90,123)`, etc.
3. **See the mixed color and its RGB value** displayed instantly below the inputs.
4. **Click any swatch label** (hex or RGB) to copy its color code to your clipboard for easy use in your projects.
5. **Explore colors with your keyboard:**
   - **Arrows:**
     - **↑ / ↓:** Increase or decrease the green channel.
     - **← / →:** Decrease or increase the red channel.
     - **Shift + ↑/↓:** Increase or decrease the blue channel.
   - This lets you fine-tune colors quickly without using your mouse.
6. **Save your favorite colors to your personal palette:**
   - Click the **+ (Add)** button to add the current color to your palette (right column).
   - The palette column appears automatically when you have saved colors, and disappears when empty for a clean look.
   - Your palette is saved for your session, so you can keep working with your favorite colors.
7. **Use or copy a palette color:**
   - Click any color swatch in your palette to instantly set it as the background color.
   - Click the color code label in your palette to copy it to your clipboard.
   - The palette never deletes colors on click—removal is always a separate action.
8. **Remove a color from your palette:**
   - Select a palette color, then click the **– (Remove)** button to delete it from your palette.
9. **Explore color combinations:**
   - The app shows suggested color combinations and swatches for the current color.
   - Click any combination to preview and use it instantly.
10. **Restore previous mixes:**
    - The history row at the top lets you quickly restore previous color mixes and palettes with a click.
11. **Keyboard Shortcuts:**
    - Use the arrows and Shift as described above for fast color navigation.
    - Press h to show hotkey help at any time.

**Tip:** The user palette is your personal color collection for the session. It adapts to your workflow—appearing only when you need it, and always ready to copy or reuse your favorite shades. Arrow key navigation makes color exploration fast and precise, perfect for designers and developers alike.

## Keyboard Shortcuts

- **Arrows (←/→/↑/↓):** Adjust the red and green channels of the current color.
- **Shift + ↑/↓:** Adjust the blue channel.
- **h:** Show hotkey help overlay.

## Installation

### Windows

#### Precompiled Installer
Download the installer from the [latest release](https://github.com/kviking/colormixer/releases). (Unsigned, but safe to install over old versions.)

#### Source Building Script
Prerequisites:

- [Git BASH](https://git-scm.com/downloads)
- [Inno Setup 6](https://jrsoftware.org/isdl.php)
- [Python 3.12](https://www.python.org/downloads/) or later
- Flet, either in a virtualenv python version or across your system with `pip install flet` [NOT recommended]

Once those are up and working, open Git BASH and navigate to the source folder. Then run our build script:

```bash
./wbuild.sh {your version number}
```

A file `ColorMixerInstaller-{your version number}.exe will be in the source folder after its completion.

#### Manually Build From Source

Install Python 3.12 or later, either install pip or run `py -m ensurepip`. You'll need to update your PATH to make python scripts callable (definitely a Google it step, many have come before me and explained it better). Once Python is up and running, it's pretty smooth sailing. Navigate to the folder with main.py in it and then run

```powershell
pip install -r requirements.txt
flet build windows .
```

In `windows/build` there will be an exe that will happily run on your system. To install it as proper program, you'll need [Inno Setup 6](https://jrsoftware.org/isdl.php). In our folder, there's a script `inno-colormixer.iss` that will build an installer for you using Inno. Once it's installed, simply run

```powershell
ISCC.exe /DVersion={your_version_number} inno-colormixer.iss
```

and it should compile an installer for you. Takes about a minute.

---

### Linux

Build from source with Python 3.12+ and run

```bash
pip install -r requirements.txt
flet build linux .
```

Also there is a bash script `wbuild` for windows builds, but could be repurposed for linux use with minor edits.

---

### Android

- Use the APK in `build/apk/` (experimental).

---

## Customization & Hacking

- All UI components are modularized in the `components/` folder for easy hacking.
- Core color logic, state, and hotkey handling are in the `core/` folder.
- Swatches and palettes are now defined in Python config (`core/config.py`).
- The user palette (custom color column) logic is now modularized in `components/user_palette.py` (extracted from `swatches.py`).
- The palette column only appears when the user palette is non-empty, and the input row's left padding dynamically adjusts for a consistent layout.
- Build scripts and installer logic are in `wbuild.sh` and `inno-colormixer.iss`.
- See the codebase and comments for developer onboarding tips.

## Build & Installer Scripts

- The `wbuild.sh` script builds, versions, and packages the app for Windows, with emoji-tagged CLI notifications.
- Use `./wbuild.sh --help` for all options, including direct notification testing.
- The installer is built with Inno Setup (`inno-colormixer.iss`).

## Testing

- Run all tests with `pytest tests/`.
- Tests use dummy classes to avoid Flet type errors and cover all major components and logic.

## Contributing

Pull requests are welcome! See the code, tests, and hacking guide for details. Bonus points for code that actually works and is tested.

## License

No formal license. If you get something out of it, I'm happy for you.

---

ColorMixer: Making the world a little brighter, one pixel at a time. Now go mix something fabulous!
