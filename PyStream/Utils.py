import yt_dlp
import re
import os
import asyncio
from YouTubeMusic.YtSearch import Search
from .Audio import AudioHandler

async def download_audio(query: str, output_format="mp3") -> str:
    search_results = await Search(query, limit=1)
    if not search_results:
        raise Exception(f"Song '{query}' not found.")

    url = search_results[0]["url"]
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "./downloads/%(id)s.%(ext)s",
        "cookiefile": "cookies/cookies.txt",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": output_format,
                "preferredquality": "192",
            }
        ],
    }

    loop = asyncio.get_event_loop()
    info = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=True))

    if not info or "requested_downloads" not in info:
        raise Exception("Download info is incomplete.")

    downloaded_file = info["requested_downloads"][0]["_filename"]
    converted_file = downloaded_file.rsplit(".", 1)[0] + f".{output_format}"

    if not os.path.exists(converted_file):
        raise Exception("Failed to convert or locate the downloaded audio file.")

    return converted_file
def validate_url(url: str) -> bool:
    youtube_pattern = r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)'
    if re.match(youtube_pattern, url):
        return True
    return False

def get_video_duration(url: str) -> int:
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('duration', 0)
      
