from pyrogram import Client, VoiceChat
from .Types import Track, QueueItem
from .Utils import download_audio, validate_url, get_video_duration
from .Exceptions import StreamException, VCJoinError, InvalidURL, QueueEmptyError
import asyncio
import os

class PyStream:
    def __init__(self, client: Client):
        self.client = client
        self.calls = {}
        self.queues = {}
        self.ffmpeg_processes = {}

    async def join(self, chat_id: str) -> VoiceChat:
        if chat_id in self.calls:
            raise VCJoinError(f"Already in a call in chat {chat_id}")

        voice_chat = VoiceChat(chat_id)
        await voice_chat.start()
        self.calls[chat_id] = voice_chat
        return voice_chat

    async def leave(self, chat_id: str) -> None:
        if chat_id in self.calls:
            voice_chat = self.calls.pop(chat_id)
            await voice_chat.stop()
        else:
            raise VCJoinError(f"Not in a voice chat for chat {chat_id}")

    async def stream(self, chat_id: str, url: str) -> None:
        if not validate_url(url):
            raise InvalidURL("Invalid URL provided.")

        try:
            track_duration = get_video_duration(url)
            track = Track(title="Track", url=url, duration=track_duration)

            queue_item = QueueItem(track=track, requested_by="User", position=1)
            self.queues.setdefault(chat_id, []).append(queue_item)

            file_path = download_audio(url)
            await self._play_audio(chat_id, file_path)

        except Exception as e:
            raise StreamException(f"Error while streaming: {str(e)}")

    async def skip(self, chat_id: str) -> None:
        if chat_id in self.queues and self.queues[chat_id]:
            self.queues[chat_id].pop(0)
            await self._start_next_track(chat_id)
        else:
            raise QueueEmptyError("The queue is empty, cannot skip.")

    async def _play_audio(self, chat_id: str, file_path: str) -> None:
        voice_chat = self.calls.get(chat_id)
        if not voice_chat:
            raise VCJoinError(f"Not in a voice chat for chat {chat_id}")

        voice_chat.play_audio(file_path)
        self.ffmpeg_processes[chat_id] = file_path

        await asyncio.sleep(10)
        self._stop_audio(chat_id)

    def _stop_audio(self, chat_id: str) -> None:
        proc = self.ffmpeg_processes.get(chat_id)
        if proc:
            del self.ffmpeg_processes[chat_id]

    async def _start_next_track(self, chat_id: str) -> None:
        if chat_id in self.queues and self.queues[chat_id]:
            next_item = self.queues[chat_id][0]
            await self._play_audio(chat_id, next_item.track.url)
          
