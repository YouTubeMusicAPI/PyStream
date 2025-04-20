from pyrogram import Client
from PyStream import PyStream
import asyncio

API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b"
SESSION = "BQBclYcAfwPhsOaYEN9rZiJTeqV1e-mW90J3pxU5lU-HRDBDir4n236Uy6xowZLnSJ83DDyV-7m8NommEpFKXVZMwRR41bXxvE8JzhIcLIJnCP5yObgE3yRkljsE36qEsdVYTgggdMSHrhoFWZG5YuOIJ0hi1HpqzOJhocARqoVbys1-CNSjTAEXdNB3knhatAqkHVnHfWcgvtshc3iiru3Gjpl9lXaPnLL5p5GP11dL8vRS4Dob-8nZW2vEkXqsD4-Ce6BAD8m4RIqTsomtrQCgaH4ugYfpFuKVr_oz04hUTjB4MzXK-Wr_Fz5Lk42PnrE3wWEwhsfgOVu8AM02YlKLV77MegAAAAHKUdR6AA"

app = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

pystream = PyStream(app)

CHAT_ID = -1002678147540
URL = "https://youtu.be/ifgr36iVY08?si=1LJvd1CENxCG9j_q"

async def main():
    await app.start()
    
    try:
        user = await app.get_me()
        print(f"Checking membership for: {user.id} ({user.first_name})")
        member = await app.get_chat_member(chat_id, user.id)
        print(f"Status: {member.status}")
        
        await app.join_chat("@tesinglele")
        print("✅ Joined chat @tesinglele")

        chat = await app.get_chat("@tesinglele")
        chat_id = chat.id
        print(f"✅ Chat ID for @tesinglele is {chat_id}")
    except Exception as e:
        print(f"[ERROR] Failed to get chat info or join chat: {e}")
        return

    try:
        await pystream.join(chat_id)
        print("✅ Joined voice chat.")
    except Exception as e:
        print(f"[ERROR] Failed to join VC: {e}")
        return

    try:
        await pystream.stream(chat_id, URL)
        print("🎶 Streaming started.")
    except Exception as e:
        print(f"[ERROR] Streaming failed: {e}")
    await asyncio.get_event_loop().create_future()

# Start the bot
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot stopped manually.")
        
