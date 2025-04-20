import yt_dlp
import re
import os
from .Audio import AudioHandler

def download_audio(url: str, output_format='mp3') -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioquality': 1,
        'outtmpl': f'./downloads/%(id)s.%(ext)s',
        'cookiefile': 'cookies/cookies.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            output_path = filename.replace(".webm", f".{output_format}")
            AudioHandler.convert_to_mp3(filename, output_path)
            if os.path.exists(filename):
                os.remove(filename)
            return output_path
    except yt_dlp.utils.DownloadError as e:
        print(f"Download error: {e}")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred during download: {e}")
        return ""


def validate_url(url: str) -> bool:
    youtube_pattern = r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=[\w-]+|youtu\.be/[\w-]+))'
    if re.search(youtube_pattern, url):
        return True
    return False


def get_video_duration(url: str) -> int:
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict.get('duration', 0)
    except yt_dlp.utils.DownloadError as e:
        print(f"Error fetching video duration: {e}")
        return 0
    except Exception as e:
        print(f"An unexpected error occurred while fetching video duration: {e}")
        return 0
