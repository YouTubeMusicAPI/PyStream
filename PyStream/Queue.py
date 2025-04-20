from typing import List
from .Types import QueueItem

class AudioQueue:
    def __init__(self):
        self.queue = []

    def add(self, item: QueueItem) -> None:
        self.queue.append(item)

    def pop(self) -> QueueItem:
        if self.queue:
            return self.queue.pop(0)
        return None

    def clear(self) -> None:
        self.queue.clear()

    def is_empty(self) -> bool:
        return len(self.queue) == 0
      
