from typing import Optional

class Track:
    def __init__(self, title: str, url: str, duration: int):
        self.title = title
        self.url = url
        self.duration = duration

class QueueItem:
    def __init__(self, track: Track, requested_by: str, position: int):
        self.track = track
        self.requested_by = requested_by
        self.position = position
      
