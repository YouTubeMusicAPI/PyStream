import asyncio
from pyrogram import Client
from .Types import Track, QueueItem
from .Utils import download_audio, validate_url, get_video_duration
from .Exceptions import StreamException, VCJoinError, InvalidURL, QueueEmptyError
from .Audio import AudioHandler


class PyStream:
    def __init__(self, client: Client):
        self.client = client
        self.calls = {}
        self.queues = {}
        self.streams = {}

    async def join(self, chat_id: int):
        if chat_id in self.calls:
            raise VCJoinError(f"Already joined voice chat in {chat_id}")
        try:
            await self.client.join_group_call(chat_id, AudioHandler.dummy_input())
            self.calls[chat_id] = True
        except Exception as e:
            raise VCJoinError(f"Error joining VC: {e}")

    async def leave(self, chat_id: int):
        if chat_id in self.calls:
            await self.client.leave_group_call(chat_id)
            self.calls.pop(chat_id)
            self._stop_audio(chat_id)
        else:
            raise VCJoinError(f"Not in VC for chat {chat_id}")

    async def stream(self, chat_id: int, url: str):
        if not validate_url(url):
            raise InvalidURL("Invalid URL provided.")

        try:
            duration = get_video_duration(url)
            track = Track(title="Track", url=url, duration=duration)
            queue_item = QueueItem(track=track, requested_by="User", position=1)
            self.queues.setdefault(chat_id, []).append(queue_item)

            await self._start_next_track(chat_id)

        except Exception as e:
            raise StreamException(f"Streaming failed: {e}")

    async def skip(self, chat_id: int):
        if chat_id in self.queues and self.queues[chat_id]:
            self.queues[chat_id].pop(0)
            await self._start_next_track(chat_id)
        else:
            raise QueueEmptyError("No more songs in queue.")

    async def _start_next_track(self, chat_id: int):
        if not (self.queues.get(chat_id) and self.queues[chat_id]):
            raise QueueEmptyError("Queue is empty.")

        next_track = self.queues[chat_id][0].track
        file_path = download_audio(next_track.url)

        await self._play_audio(chat_id, file_path)

    async def _play_audio(self, chat_id: int, file_path: str):
        self._stop_audio(chat_id)

        try:
            proc = AudioHandler.stream_audio(chat_id, file_path)
            self.streams[chat_id] = proc
        except Exception as e:
            raise StreamException(f"Audio playback failed: {e}")

    def _stop_audio(self, chat_id: int):
        if chat_id in self.streams:
            self.streams[chat_id].kill()
            del self.streams[chat_id]
