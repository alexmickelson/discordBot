import os
import yt_dlp
import glob
from src.models import SongMetadata, SongItem

DATA_PATH = "/tmp/songs"

def handle_metadata(filename: str, song_duration: int, url: str):
    json_path = filename.rsplit(".", 1)[0] + ".json"
    thumbnail_path = filename.rsplit(".", 1)[0] + ".jpg"
    thumbnail_filename = os.path.basename(thumbnail_path)
    song_metadata = SongMetadata(
        filename=filename,
        duration=song_duration,
        url=url,
        thumbnail=thumbnail_filename,
    )
    with open(json_path, "w") as f:
        f.write(song_metadata.model_dump_json())

def download_url(url: str):
    print("in download url")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DATA_PATH}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "nooverwrites": False,
        "writethumbnail": True,  # Download thumbnail as well
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {"key": "FFmpegThumbnailsConvertor", "format": "jpg"},
        ],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            res = ydl.extract_info(url)
            if res is None:
                raise ValueError("yt_dlp failed to extract info for the given URL.")
            filename = ydl.prepare_filename(res).rsplit(".", 1)[0] + ".mp3"
            song_duration = res["duration"]
            print(f"got file {filename} {song_duration}")
            handle_metadata(filename, song_duration, url)
            return filename, song_duration
    except Exception as e:
        print(f"Error in download: {e}")
        raise

def get_all_songs():
    all_songs_list = []
    for json_path in glob.glob(f"{DATA_PATH}/*.json"):
        try:
            with open(json_path, "r") as f:
                data = f.read()
                song_metadata = SongMetadata.model_validate_json(data)
                all_songs_list.append(song_metadata)
        except Exception as e:
            print(f"Failed to load {json_path}: {e}")
    return all_songs_list
