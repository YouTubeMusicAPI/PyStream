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
        await app.send_message(CHAT_USERNAME, "✅ Music bot has started and is ready to play music!")

        chat = await app.get_chat("@tesinglele")
        print(f"✅ Chat ID for @tesinglele is {chat.id}")
        
        member = await app.get_chat_member("@tesinglele", app.me.id)
        print(f"✅ Membership check: {member.status}")
        
        if member.status in ["member", "administrator"]:
            print("✅ Userbot is a member and has permissions.")
            
            try:
                await app.join_voice_chat(chat.id)
                print("✅ Joined voice chat successfully.")
            except Exception as e:
                print(f"[ERROR] Failed to join voice chat: {str(e)}")

            await pystream.stream(chat.id, URL)
            print("✅ Music bot is running.")

        else:
            print("[ERROR] Userbot is not a member or admin in the group.")

    except Exception as e:
        print(f"[ERROR] Failed to join or stream: {str(e)}")
    
    await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Userbot stopped manually.")
