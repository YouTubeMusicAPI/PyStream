import asyncio
import asyncio
from pyrogram import Client
from PyStream.Exceptions import VCJoinError
from PyStream.Utils import download_audio, validate_url
import subprocess
import os

class PyStream:
    def __init__(self, client: Client):
        self.client = client
        self.calls = {}
        self.queues = {}
        self.streams = {}
        self.active_chats = set()

    async def join(self, chat_id: int):
        if chat_id in self.calls:
            raise VCJoinError(f"Already joined voice chat in {chat_id}")
        
        try:
            await self.client.send_message(chat_id, "Joining voice chat")
            self.calls[chat_id] = True
            self.active_chats.add(chat_id)

        except Exception as e:
            raise VCJoinError(f"Error joining VC: {e}")

    async def leave(self, chat_id: int):
        if chat_id in self.calls:
            await self.client.send_message(chat_id, "Leaving voice chat")
            self.calls.pop(chat_id)
            self._stop_audio(chat_id)
            self.active_chats.discard(chat_id)
        else:
            raise VCJoinError(f"Not in VC for chat {chat_id}")

    def is_active(self, chat_id: int):
        return chat_id in self.active_chats

    async def stream(self, chat_id: int, url: str):
        if not validate_url(url):
            raise Exception("Invalid URL provided.")

        try:
            file_path = download_audio(url)
            await self._play_audio(chat_id, file_path)

        except Exception as e:
            raise VCJoinError(f"Streaming failed: {e}")

    async def _play_audio(self, chat_id: int, file_path: str):
        self._stop_audio(chat_id)
        try:
            process = subprocess.Popen(
                ["ffmpeg", "-i", file_path, "-f", "opus", "-ar", "48000", "-ac", "2", "-b:a", "128k", "-vn", "-"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.streams[chat_id] = process
        except Exception as e:
            raise VCJoinError(f"Audio playback failed: {e}")

    def _stop_audio(self, chat_id: int):
        if chat_id in self.streams:
            process = self.streams[chat_id]
            process.terminate()
            self.streams.pop(chat_id)
            os.remove(process.stdout.name)

    def is_active(self, chat_id: int):
        return chat_id in self.active_chats
