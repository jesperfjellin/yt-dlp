import subprocess
import json
import sys
import os

def get_video_info(url):
    """
    Fetch video information using yt-dlp without downloading the video.
    
    Parameters:
    - url: The URL of the video.
    
    Returns:
    A dictionary containing video information.
    """
    command = ['yt-dlp', '--print-json', '--simulate', url]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        print("Error fetching video information.")
        print(result.stderr)
        sys.exit(1)

def format_size(size):
    """
    Convert size in bytes to a more readable format.
    
    Parameters:
    - size: File size in bytes.
    
    Returns:
    A string representing the file size in KB, MB, or GB.
    """
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

def download_video(url, default_path='C:\\Python\\yt-dlp\\movies'):
    print(f"Downloading: {url}")
    info = get_video_info(url)
    if 'filesize_approx' in info:
        size = format_size(info['filesize_approx'])
    else:
        size = "Unknown"
    
    print(f"Title: {info.get('title', 'Unknown')}")
    print(f"Size: {size}")
    
    # Ask the user to confirm or change the default save location
    print(f"Default save location is '{default_path}'. Is this okay? [y/n]")
    save_location_okay = input().strip().lower()
    if save_location_okay != 'y':
        default_path = input("Enter new download path: ")
    
    if save_location_okay == 'y':
        # Ensure the new or default directory exists
        if not os.path.exists(default_path):
            os.makedirs(default_path)
        # Set the output template for yt-dlp
        output_template = os.path.join(default_path, '%(title)s.%(ext)s')
        subprocess.run(['yt-dlp', '-k', '-o', output_template, url])
    else:
        print("Download canceled.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
        download_video(video_url)
    else:
        print("Usage: python yt-dlp.py <video_url>")
