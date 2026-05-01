# WalleRotator 🖼️

A lightweight, zero-dependency Windows desktop wallpaper rotator written in Python. It runs invisibly in the background, consuming practically zero CPU/RAM, and automatically updates your desktop background at a customizable interval.

## ✨ Features

- **Reddit Integration**: Automatically scrapes the "Top 10 of the day" posts from any subreddit (e.g., `r/wallpapers`, `r/EarthPorn`) and sets a random high-quality image as your desktop background.
- **Local Folder Support**: Prefer your own images? You can easily configure it to randomly cycle through a local folder of `.jpg` or `.png` files instead.
- **Zero-Dependency Core**: Uses native Windows `ctypes` (`SystemParametersInfoW`) to change the background without needing heavy 3rd-party libraries.
- **Fully Portable & Universal**: 
  - Automatically resolves to your universal `Pictures` folder (`C:\Users\YourUser\Pictures\WalleRotator`) to store configs and downloads.
  - Automatically adds itself to the Windows Startup folder on the very first run.
- **JSON Configuration**: Highly customizable via a simple `config.json` file.

## ⚙️ Configuration

When you run the script for the first time, it will automatically generate a `config.json` file in your `Pictures\WalleRotator` folder. 

```json
{
    "source": "reddit",  
    "wallpaper_dir": "C:\\Users\\YourUser\\Pictures\\WalleRotator\\wallpapers",
    "interval_seconds": 3600,
    "subreddit": "wallpapers"
}
```
- `source`: Set to `"reddit"` to pull from Reddit or `"local"` to pull from your local `wallpaper_dir`.
- `subreddit`: Which subreddit to scrape images from.
- `interval_seconds`: How often the wallpaper changes (e.g., `3600` for 1 hour).

## 🚀 How to Run

### Option 1: Run as a Python Script
If you have Python installed, simply run:
```bash
python wallpaper_rotator.pyw
```
*(Note: the `.pyw` extension ensures it runs in the background without opening a visible command prompt window).*

### Option 2: Run as a Portable Executable
You can compile this script into a standalone `.exe` so you can share it with friends who don't have Python installed.

1. Install PyInstaller:
```bash
pip install pyinstaller
```
2. Build the `.exe`:
```bash
pyinstaller --noconsole --onefile --name wallrote wallpaper_rotator.pyw
```
3. Your portable executable will be generated in the `dist/` folder. Just double-click `wallrote.exe` and it will automatically handle the rest, including adding itself to your Windows Startup!
