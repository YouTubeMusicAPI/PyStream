import subprocess
import os
from tempfile import NamedTemporaryFile

class AudioHandler:
    @staticmethod
    def convert_to_mp3(input_file: str, output_file: str) -> None:
        try:
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-vn', '-acodec', 'libmp3lame', '-ab', '192k',
                output_file
            ]
            subprocess.run(cmd, check=True)
            print(f"Conversion successful: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")

    @staticmethod
    def stream_audio(input_file: str, output_file: str) -> None:
        try:
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-f', 'opus', '-acodec', 'libopus', '-vn', '-ar', '48000', '-ac', '2', '-b:a', '96k',
                output_file
            ]
            subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Streaming started for {output_file}")
        except Exception as e:
            print(f"Error during streaming: {e}")

    @staticmethod
    def create_temp_file() -> str:
        try:
            temp_file = NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()  # Ensure the file is created and closed before returning
            return temp_file.name
        except Exception as e:
            print(f"Error creating temporary file: {e}")
            return ""
            
