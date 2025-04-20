import yt_dlp
import re
import os
from YouTubeMusic.YtSearch import Search
from .Audio import AudioHandler

async def download_audio(query: str, output_format='mp3') -> str:
    search_results = await Search(query, limit=1)
    if not search_results:
        raise Exception(f"Song '{query}' not found.")
    
    url = search_results[0]["url"]

    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioquality': 1,
        'outtmpl': './downloads/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }],
        'cookiefile': cookies/cookies.txt,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(data)
            output_path = filename.replace(".webm", f".{output_format}")
            AudioHandler.convert_to_mp3(filename, output_path)
            os.remove(filename)
    except Exception as e:
        raise Exception(f"Error downloading the song: {e}")

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
      
