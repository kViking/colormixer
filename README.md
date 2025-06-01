# 🎨 ColorMixer

ColorMixer lets you blend, explore, and copy colors with a clean, fast, and cross-platform interface. Whether you're a designer, developer, or just love color, this app is for you.

## Features

- **Mix Colors Instantly:** Enter two colors in any format (hex, RGB, with or without #, spaces or commas) and see the result.
- **Clickable Swatch Labels:** Click the color code in any swatch to copy or trigger actions—no more fiddling to grab a hex code.
- **Palette Exploration:** Instantly see and navigate color combinations and swatches.
- **Hotkey Navigation:** Use arrow keys (and Shift) to explore the RGB color space without leaving your keyboard.
- **Cross-Platform:** Works on Linux, Windows, and Android. (Mac support coming soon!)
- **Minimalist UI:** No clutter, just color. Designed for speed and clarity.
- **History:** Quickly restore previous mixes and palettes.

## How to Use

1. Open the app.
2. Enter two colors (any format: `#4edec1`, `4edec1`, `78, 90, 123`, `(78,90,123)`, etc.).
3. See the mixed color and its RGB value.
4. Click any swatch label to copy its color code.
5. Use arrow keys to explore color variations.

- ↑/↓ to adjust green
- ←/→ to adjust red
- Shift + ↑/↓ to adjust blue

## Keyboard Shortcuts

- **Arrow Keys:** Adjust the red/green channels.
- **Shift + Up/Down:** Adjust the blue channel.
- **Tab:** Show hotkey help.

## Installation

### Windows

- Download the installer from the [latest release](https://github.com/kviking/colormixer/releases). (Unsigned, but safe to install over old versions.)

### Linux

- Build from source with Python 3.12+ and `pip install -r requirements.txt`, then `flet build linux .`

### Android

- Use the APK in `build/apk/` (experimental).

## Customization & Hacking

- All UI components are modularized in the `components/` folder for easy hacking.
- Swatches and palettes are defined in `swatches.json`—add your own!
- Build scripts and installer logic are in `wbuild.sh` and `inno-colormixer.iss`.

## Contributing

Pull requests are welcome! See the code, tests, and hacking guide for details. Bonus points for code that actually works.

## License

No formal license. If you get something out of it, I'm happy for you.

---

ColorMixer: Making the world a little brighter, one pixel at a time. Now go mix something fabulous!
