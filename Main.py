import asyncio
from pathlib import Path

from PyStream.Utils import download_audio

async def main():
    query = input("🎵 Enter song name or URL: ") or "Chandni"
    print(f"🔎 Searching and downloading: {query}")
    
    try:
        path = await download_audio(query)
        print(f"✅ Downloaded and saved to: {path}")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    # Ensure downloads folder exists
    Path("downloads").mkdir(parents=True, exist_ok=True)
    asyncio.run(main())
  
