import asyncio
import os
from typing import Union
from pyrogram import Client
from .Audio import AudioHandler
from .Types import Track, QueueItem
from .Utils import download_audio, validate_url, get_video_duration
from .Exceptions import StreamException, VCJoinError, InvalidURL, QueueEmptyError


class PyStream:
    def __init__(self, client: Client):
        self.client = client
        self.calls = {}
        self.queues = {}
        self.ffmpeg_processes = {}

    async def join(self, chat_id: Union[int, str]) -> None:
        try:
            if chat_id in self.calls:
                raise VCJoinError(f"Already in a call in chat {chat_id}")

            chat_member = await self.client.get_chat_member(chat_id, self.client.me.id)
            if chat_member.status not in ["member", "administrator"]:
                raise VCJoinError(f"Bot is not a member of chat {chat_id}")
            
            self.calls[chat_id] = True
            print(f"[JOIN] Successfully joined VC in {chat_id}")
            
            chat = await self.client.get_chat(chat_id)
            if not chat or not chat.type == "supergroup" or not chat.permissions.can_send_messages:
                raise VCJoinError(f"Bot cannot join the VC in chat {chat_id} due to permissions or chat type.")

            await asyncio.sleep(2)
            
        except VCJoinError as e:
            print(f"[ERROR] {str(e)}")
        except Exception as e:
            print(f"[ERROR] Failed to join VC in {chat_id}: {str(e)}")

    async def leave(self, chat_id: str) -> None:
        if chat_id in self.calls:
            await self.stop_audio(chat_id)
            self.calls.pop(chat_id, None)
            print(f"[LEAVE] {chat_id}")
        else:
            raise VCJoinError(f"Not in a voice chat for chat {chat_id}")

    async def stream(self, chat_id: Union[int, str], url: str) -> None:
        if not validate_url(url):
            raise InvalidURL("Invalid URL provided.")
        try:
            await self.join(chat_id)
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
        if chat_id not in self.calls:
            raise VCJoinError(f"Not in a voice chat for chat {chat_id}")
        temp_output = AudioHandler.create_temp_file()
        AudioHandler.stream_audio(file_path, temp_output)
        self.ffmpeg_processes[chat_id] = temp_output
        print(f"[PLAY] {chat_id}")
        await asyncio.sleep(10)
        await self.stop_audio(chat_id)

    async def stop_audio(self, chat_id: str) -> None:
        output_file = self.ffmpeg_processes.get(chat_id)
        if output_file and os.path.exists(output_file):
            os.remove(output_file)
            print(f"[STOP] {chat_id}")
        self.ffmpeg_processes.pop(chat_id, None)

    async def _start_next_track(self, chat_id: str) -> None:
        if chat_id in self.queues and self.queues[chat_id]:
            next_item = self.queues[chat_id][0]
            file_path = download_audio(next_item.track.url)
            await self._play_audio(chat_id, file_path)
