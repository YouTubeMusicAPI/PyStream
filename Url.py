import yt_dlp
import os

def download_audio(url: str, output_format='mp3') -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioquality': 1,
        'outtmpl': f'./downloads/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            output_path = filename.replace(".webm", f".{output_format}")
            
            # Check if the .webm file exists before trying to delete it
            if os.path.exists(filename):
                os.remove(filename)
                
            return output_path

    except Exception as e:
        print(f"Error downloading or converting audio: {e}")
        return None

url = "https://youtu.be/bVNJVB10C6w?si=kqUhtB9yZ5Da83lk"  # Replace with the actual URL you want

downloaded_file = download_audio(url)
if downloaded_file:
    print(f"Audio downloaded successfully: {downloaded_file}")
else:
    print("Failed to download audio.")
    
