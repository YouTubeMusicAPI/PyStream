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

async def get_stream_url(query: str) -> str:
    search_results = await Search(query, limit=1)
    if not search_results:
        raise Exception(f"❌ Song '{query}' not found.")
    url = search_results[0]["url"]
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: YoutubeDL(YDL_OPTS).extract_info(url, download=False))
    if "url" not in data:
        raise Exception(f"❌ Failed to extract stream URL for '{query}'.")
    return data["url"], search_results[0]["title"]

@app.on_message(filters.command("play") & filters.group)
async def play_song(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Please provide a song name to play.")
    query = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    try:
        stream_url, title = await get_stream_url(query)
        if not vc.is_active(chat_id):
            await message.reply("🎧 Joining voice chat...")
            await vc.join(chat_id)
            await vc.stream(chat_id, stream_url)
            return await message.reply(f"▶️ Playing: {title}")
        else:
            queue.add(chat_id, stream_url)
            return await message.reply(f"➕ Queued: {title}")
    except Exception as e:
        return await message.reply(str(e))


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
