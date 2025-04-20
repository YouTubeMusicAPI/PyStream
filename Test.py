from pyrogram import Client
from PyStream import PyStream
import asyncio

API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b"
SESSION = "BQBclYcAfwPhsOaYEN9rZiJTeqV1e-mW90J3pxU5lU-HRDBDir4n236Uy6xowZLnSJ83DDyV-7m8NommEpFKXVZMwRR41bXxvE8JzhIcLIJnCP5yObgE3yRkljsE36qEsdVYTgggdMSHrhoFWZG5YuOIJ0hi1HpqzOJhocARqoVbys1-CNSjTAEXdNB3knhatAqkHVnHfWcgvtshc3iiru3Gjpl9lXaPnLL5p5GP11dL8vRS4Dob-8nZW2vEkXqsD4-Ce6BAD8m4RIqTsomtrQCgaH4ugYfpFuKVr_oz04hUTjB4MzXK-Wr_Fz5Lk42PnrE3wWEwhsfgOVu8AM02YlKLV77MegAAAAHKUdR6AA"

app = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

pystream = PyStream(app)

CHAT_ID = "-1002678147540"
URL = "https://youtu.be/ifgr36iVY08?si=1LJvd1CENxCG9j_q"

async def main():
    await app.start()
    await pystream.stream(CHAT_ID, URL)
    await asyncio.sleep(15)
    await pystream.leave(CHAT_ID)
    await app.stop()

app.run(main())
