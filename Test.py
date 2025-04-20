from pyrogram import Client, filters, idle
from PyStream.Client import PyStream
from PyStream.Queue import AudioQueue
from YouTubeMusic.YtSearch import Search
from yt_dlp import YoutubeDL
import asyncio

API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b"
SESSION = "BQBclYcAfwPhsOaYEN9rZiJTeqV1e-mW90J3pxU5lU-HRDBDir4n236Uy6xowZLnSJ83DDyV-7m8NommEpFKXVZMwRR41bXxvE8JzhIcLIJnCP5yObgE3yRkljsE36qEsdVYTgggdMSHrhoFWZG5YuOIJ0hi1HpqzOJhocARqoVbys1-CNSjTAEXdNB3knhatAqkHVnHfWcgvtshc3iiru3Gjpl9lXaPnLL5p5GP11dL8vRS4Dob-8nZW2vEkXqsD4-Ce6BAD8m4RIqTsomtrQCgaH4ugYfpFuKVr_oz04hUTjB4MzXK-Wr_Fz5Lk42PnrE3wWEwhsfgOVu8AM02YlKLV77MegAAAAHKUdR6AA"

app = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

vc = PyStream(app)
queue = AudioQueue()

"""
YDL_OPTS = {
    "format": "bestaudio[ext=m4a]/bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "nocheckcertificate": True,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0",
    "forceipv4": True,
    "cachedir": False,
    "cookiefile": "cookies/cookies.txt",
}

async def get_stream_url(query: str) -> tuple[str, str]:
    print(f"[🔍] Searching for: {query}")
    
    results = await Search(query, limit=1)
    print(f"[📦] Search results: {results}")
    
    if not results:
        raise Exception(f"❌ No results found for: {query}")
    
    result = results[0]
    url = result.get("url")
    title = result.get("title", "Unknown Title")

    print(f"[✅] Found YouTube URL: {url}")
    print(f"[🎵] Title: {title}")

    if not url:
        raise Exception("❌ No URL found in the result.")
    
    loop = asyncio.get_event_loop()
    print("[⏳] Extracting stream URL using yt-dlp...")
    
    data = await loop.run_in_executor(None, lambda: YoutubeDL(YDL_OPTS).extract_info(url, download=False))
    
    print(f"[📡] yt-dlp data: {data.keys() if isinstance(data, dict) else data}")
    
    if not isinstance(data, dict) or "url" not in data:
        raise Exception(f"❌ Failed to extract stream URL for: {query}")
    
    stream_url = data["url"]
    print(f"[🎧] Final Stream URL: {stream_url}")
    
    return stream_url, title
"""

import yt_dlp

async def get_stream_url(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioquality': 1,
        'quiet': True,
        'noplaylist': True,
        'cookiefile': 'cookies/cookies.txt',
    }
    search_query = f"ytsearch:{query}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Perform the search and get the results
            info_dict = ydl.extract_info(search_query, download=False)
            
            # Check if the video entries are available
            if 'entries' in info_dict and len(info_dict['entries']) > 0:
                # Get the first video from the search result
                video_url = info_dict['entries'][0].get('url')
                title = info_dict['entries'][0].get('title')
                
                if video_url:
                    return video_url, title
                else:
                    print("[❌] Error: URL not found in the search result.")
                    return None, None
            else:
                print("[❌] Error: No entries found.")
                return None, None
        except Exception as e:
            print(f"[❌] Error searching for song: {e}")
            return None, None
            
@app.on_message(filters.command("play") & filters.group)
async def play_song(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Please provide a song name.")
    
    query = message.text.split(None, 1)[1]
    chat_id = message.chat.id

    try:
        print(f"[🔍] Searching for: {query}")
        stream_url, title = await get_stream_url(query)
        
        # Debugging: Log the URL
        print(f"[🎵] Stream URL: {stream_url}")

        # Check if stream_url is valid
        if not stream_url:
            raise Exception("Invalid URL provided.")
        
        # Streaming process
        if not vc.is_active(chat_id):
            await vc.join(chat_id)
            await vc.stream(chat_id, stream_url)
            print(f"[🎧] Now Streaming: {title}")
            await message.reply(f"▶️ Now Playing: {title}")
        else:
            # If voice chat is already active, add to queue
            queue.add(chat_id, stream_url)
            print(f"[➕] Added to Queue: {title}")
            await message.reply(f"➕ Added to Queue: {title}")
    
    except Exception as e:
        print(f"[❌] Error: {str(e)}")
        return await message.reply(f"❌ Error: {str(e)}")


@app.on_message(filters.command("skip") & filters.group)
async def skip_song(client, message):
    chat_id = message.chat.id

    if queue.exists(chat_id):
        next_track = queue.pop(chat_id)
        await vc.stream(chat_id, next_track)
        await message.reply(f"⏭ Now playing: {next_track.title}")
    else:
        await vc.leave(chat_id)
        await message.reply("❌ Queue empty. Left VC.")

@app.on_message(filters.command("stop") & filters.group)
async def stop_playing(client, message):
    chat_id = message.chat.id
    await vc.leave(chat_id)
    queue.clear(chat_id)
    await message.reply("⏹ Stopped music and left VC.")

async def main():
    await app.start()
    print("🎶 PyStream Music UserBot running...")
    await idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
