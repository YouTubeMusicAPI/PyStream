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
        'postprocessors': [{
            'key': 'FFmpegAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        output_path = filename.replace(".webm", f".{output_format}")
        AudioHandler.convert_to_mp3(filename, output_path)
        os.remove(filename)
        return output_path

def validate_url(url: str) -> bool:
    youtube_pattern = r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)'
    if re.match(youtube_pattern, url):
        return True
    return False

def get_video_duration(url: str) -> int:
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('duration', 0)
      
