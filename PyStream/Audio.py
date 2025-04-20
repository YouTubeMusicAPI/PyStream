import subprocess
import os
from tempfile import NamedTemporaryFile

class AudioHandler:
    @staticmethod
    def convert_to_mp3(input_file: str, output_file: str) -> None:
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vn', '-acodec', 'libmp3lame', '-ab', '192k',
            output_file
        ]
        subprocess.run(cmd, check=True)

    @staticmethod
    def stream_audio(input_file: str, output_file: str) -> None:
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-f', 'opus', '-acodec', 'libopus', '-vn', '-ar', '48000', '-ac', '2', '-b:a', '96k',
            output_file
        ]
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    def create_temp_file() -> str:
        temp_file = NamedTemporaryFile(delete=False, suffix='.mp3')
        return temp_file.name
      
