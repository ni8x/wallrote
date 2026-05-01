# WallRote 🖼️

A lightweight, zero-dependency Windows desktop wallpaper rotator written in Python. It runs invisibly in the background, consuming practically zero CPU/RAM, and automatically updates your desktop background at a customizable interval.

## ✨ Features

*   **Reddit & Local Support**: Cycle through your own photos or automatically grab top-tier shots from subreddits like `r/EarthPorn`.
*   **Invisible & Efficient**: Written in Python using `ctypes` to talk directly to Windows—no heavy libraries, no open terminal windows.
*   **Zero Setup**: On the first run, it creates its own folders in your `Pictures` directory and adds itself to your Windows Startup automatically.
*   **Simple Config**: Everything from the subreddit source to the rotation interval is handled in a clean `config.json`.
*   
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
If you just want it to work without touching any code:
1.  Go to the **[Releases](https://github.com/ni8x/wallrote/releases)** section of this repo.
2.  Download `wallrote.exe`.
3.  Double-click to run. It will handle the rest.
