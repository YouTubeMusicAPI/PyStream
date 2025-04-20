import asyncio
from pyrogram import Client, filters, idle
from PyStream.Client import PyStream
from PyStream.Types import Track
from PyStream.Queue import AudioQueue
from PyStream.Utils import get_video_duration  # Import utility function for fetching video duration

API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b"
SESSION = "BQBclYcAfwPhsOaYEN9rZiJTeqV1e-mW90J3pxU5lU-HRDBDir4n236Uy6xowZLnSJ83DDyV-7m8NommEpFKXVZMwRR41bXxvE8JzhIcLIJnCP5yObgE3yRkljsE36qEsdVYTgggdMSHrhoFWZG5YuOIJ0hi1HpqzOJhocARqoVbys1-CNSjTAEXdNB3knhatAqkHVnHfWcgvtshc3iiru3Gjpl9lXaPnLL5p5GP11dL8vRS4Dob-8nZW2vEkXqsD4-Ce6BAD8m4RIqTsomtrQCgaH4ugYfpFuKVr_oz04hUTjB4MzXK-Wr_Fz5Lk42PnrE3wWEwhsfgOVu8AM02YlKLV77MegAAAAHKUdR6AA"

app = Client("MusicBotUser", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

vc = PyStream(app)
queue = AudioQueue()

@app.on_message(filters.command("play") & filters.group)
async def play_song(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Send a YouTube or audio URL.")

    url = message.command[1]
    chat_id = message.chat.id

    try:
        # Manually create Track object with title and duration
        track_duration = get_video_duration(url)  # Get duration using utility function
        track = Track(title="Track", url=url, duration=track_duration)
    except Exception as e:
        return await message.reply(f"❌ Error: {e}")

    if not vc.is_active(chat_id):
        await vc.join(chat_id)
        await vc.stream(chat_id, track)
        await message.reply(f"▶️ Playing: {track.title}")
    else:
        queue.add(chat_id, track)
        await message.reply(f"➕ Queued: {track.title}")

@app.on_message(filters.command("skip") & filters.group)
async def skip_song(client, message):
    chat_id = message.chat.id

    if queue.exists(chat_id):
        next_track = queue.pop(chat_id)
        await vc.stream(chat_id, next_track)
        await message.reply(f"⏭ Now playing: {next_track.title}")
    else:
        await vc.leave(chat_id)
        await message.reply("❌ Queue empty. Leaving VC.")

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
