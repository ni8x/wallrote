import os
import time
import random
import ctypes
import json
import urllib.request
import urllib.error
import sys
import subprocess

# Define base directory in user's Pictures folder
BASE_DIR = os.path.join(os.path.expanduser("~"), "Pictures", "WalleRotator")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
DEFAULT_WALLPAPER_DIR = os.path.join(BASE_DIR, "wallpapers")

def add_to_startup():
    """
    Checks if running as a compiled exe and adds a shortcut to the Windows startup folder if missing.
    """
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable
        startup_dir = os.path.join(os.getenv('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        if not startup_dir:
            return
            
        shortcut_path = os.path.join(startup_dir, 'wallrote.lnk')
        
        if not os.path.exists(shortcut_path):
            try:
                ps_script = f'$s=(New-Object -COM WScript.Shell).CreateShortcut("{shortcut_path}");$s.TargetPath="{exe_path}";$s.Save()'
                # Use CREATE_NO_WINDOW (0x08000000) to prevent the console from flashing briefly
                subprocess.run(["powershell", "-Command", ps_script], creationflags=0x08000000)
            except Exception as e:
                print(f"Error creating startup shortcut: {e}")

def load_config():
    # Default configuration
    config = {
        "source": "reddit",  # "local" or "reddit"
        "wallpaper_dir": DEFAULT_WALLPAPER_DIR,
        "interval_seconds": 3600,
        "subreddit": "wallpapers"
    }
    
    # Create default config if it doesn't exist
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error creating config: {e}")
        return config

    # Load existing config
    try:
        with open(CONFIG_FILE, 'r') as f:
            user_config = json.load(f)
            # Update default with user settings
            config.update(user_config)
    except Exception as e:
        print(f"Error reading config: {e}")
        
    return config

def get_local_wallpapers(directory):
    """
    Scans the given directory for .jpg and .png files.
    """
    if not os.path.exists(directory):
        return []
    
    valid_extensions = ('.jpg', '.jpeg', '.png')
    wallpapers = []
    
    for file in os.listdir(directory):
        if file.lower().endswith(valid_extensions):
            wallpapers.append(os.path.join(directory, file))
            
    return wallpapers

def fetch_reddit_wallpaper(subreddit, download_dir):
    """
    Fetches the top 10 posts of the day from a subreddit, picks a random JPG,
    downloads it to the specified directory, and returns the path.
    """
    url = f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit=10"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 WalleRotator/1.0'
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            # Extract posts
            children = data.get('data', {}).get('children', [])
            
            # Filter for jpg/jpeg
            valid_posts = []
            for child in children:
                post_data = child.get('data', {})
                post_url = post_data.get('url', '')
                # Ensure it's a direct image link
                if post_url.lower().endswith(('.jpg', '.jpeg', '.png')):
                    valid_posts.append(post_url)
            
            if not valid_posts:
                print(f"No valid images found in top 10 posts of r/{subreddit}.")
                return None
                
            # Choose a random image url from the top 10
            chosen_url = random.choice(valid_posts)
            
            # Create download dir if it doesn't exist
            os.makedirs(download_dir, exist_ok=True)
            
            # Extract filename from url
            filename = chosen_url.split('/')[-1]
            # Handle cases where url might have parameters like ?width=...
            filename = filename.split('?')[0] 
            
            download_path = os.path.join(download_dir, f"reddit_{filename}")
            
            # Download the image
            img_req = urllib.request.Request(chosen_url, headers=headers)
            with urllib.request.urlopen(img_req) as img_response, open(download_path, 'wb') as out_file:
                out_file.write(img_response.read())
                
            print(f"Successfully downloaded reddit image: {download_path}")
            return download_path
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error fetching from reddit: {e.code} - {e.reason}")
    except Exception as e:
        print(f"Error fetching from reddit: {e}")
        
    return None

def fetch_wallpaper(config):
    """
    Modular function to get a wallpaper based on config.
    """
    source = config.get('source', 'local').lower()
    wallpaper_dir = config.get('wallpaper_dir', DEFAULT_WALLPAPER_DIR)
    
    if source == 'reddit':
        subreddit = config.get('subreddit', 'wallpapers')
        wallpaper = fetch_reddit_wallpaper(subreddit, wallpaper_dir)
        if wallpaper:
            return wallpaper
        print("Falling back to local wallpapers due to Reddit fetch failure.")
        
    # Default to local
    wallpapers = get_local_wallpapers(wallpaper_dir)
    
    if not wallpapers:
        print(f"No wallpapers found in {wallpaper_dir}")
        return None
        
    return random.choice(wallpapers)

def set_wallpaper_windows(image_path):
    """
    Sets the Windows desktop background using native ctypes for zero-dependency execution.
    """
    # 20 = SPI_SETDESKWALLPAPER
    # 3 = SPIF_UPDATEINIFILE (1) | SPIF_SENDWININICHANGE (2)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    print(f"Wallpaper set to: {image_path}")

def main():
    # Attempt to add to startup if frozen (.exe)
    add_to_startup()
    
    while True:
        try:
            config = load_config()
            wallpaper_path = fetch_wallpaper(config)
            
            if wallpaper_path:
                set_wallpaper_windows(wallpaper_path)
                
            interval = config.get('interval_seconds', 3600)
            # Ensure interval is a number and at least somewhat reasonable (e.g. minimum 10 seconds)
            if not isinstance(interval, (int, float)) or interval < 10:
                interval = 3600
                
            print(f"Sleeping for {interval} seconds...")
            time.sleep(interval)
            
        except Exception as e:
            # Sleep a bit to prevent a tight loop on continuous errors
            print(f"Main loop error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
