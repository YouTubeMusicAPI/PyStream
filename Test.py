from pyrogram import Client
from PyStream import PyStream
import asyncio

API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b"
BOT_TOKEN = "7913409153:AAEvv86Q96KqjU6-fvj_JOBKp4_MHH9H4Wk"
SESSION = "BQBclYcAfwPhsOaYEN9rZiJTeqV1e-mW90J3pxU5lU-HRDBDir4n236Uy6xowZLnSJ83DDyV-7m8NommEpFKXVZMwRR41bXxvE8JzhIcLIJnCP5yObgE3yRkljsE36qEsdVYTgggdMSHrhoFWZG5YuOIJ0hi1HpqzOJhocARqoVbys1-CNSjTAEXdNB3knhatAqkHVnHfWcgvtshc3iiru3Gjpl9lXaPnLL5p5GP11dL8vRS4Dob-8nZW2vEkXqsD4-Ce6BAD8m4RIqTsomtrQCgaH4ugYfpFuKVr_oz04hUTjB4MzXK-Wr_Fz5Lk42PnrE3wWEwhsfgOVu8AM02YlKLV77MegAAAAHKUdR6AA"


bot = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
app = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
pystream = PyStream(app)

CHAT_USERNAME = "@tesinglele"
URL = "https://youtu.be/ifgr36iVY08?si=1LJvd1CENxCG9j_q"

async def main():
    await app.start()

    try:
        abhi = await app.send_message(CHAT_USERNAME, "✅ Music bot has started and is ready to play music!")
        print(abhi)
        
        chat = await app.get_chat(CHAT_USERNAME)
        chat_id = chat.id
        print(f"✅ Chat ID for {CHAT_USERNAME} is {chat_id}")

        user = await app.get_me()
        member = await app.get_chat_member(chat_id, user.id)
        print(f"✅ Membership check: {member.status}")
        try:
            await app.join_voice_chat(chat.id)
            print("✅ Joined voice chat successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to get chat info or join chat: {e}")
        return

    try:
        await pystream.join(CHAT_USERNAME)
        print("✅ Joined voice chat.")
        await pystream.stream(CHAT_USERNAME, URL)
    except Exception as e:
        print(f"[ERROR] Streaming failed: {e}")

    print("✅ Music bot running.")
    await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
