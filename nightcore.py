from __future__ import unicode_literals
import youtube_dl
import requests
import random
from bs4 import BeautifulSoup
import shutil
from pydub import AudioSegment
import moviepy.editor as mpe
import sys
from youtube_search import YoutubeSearch 
import json
import os


if len(sys.argv) < 2:
    print("You need to specify a search term")
    sys.exit(1)

def download_video(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }],
        "outtmpl": "audio.mp3"
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def get_random_image():
    image_number = random.randint(0, 5000)
    url = f"https://safebooru.org/index.php?page=post&s=view&id={image_number}"

    data = requests.get(url).content
    soup = BeautifulSoup(data, "html.parser")
    image_tag = soup.find(id="image")

    if not image_tag:
        print("Couldn't find image, try again")
        sys.exit(1)

    image_url = image_tag['src']
    
    image_data = requests.get(image_url, stream=True)

    with open("image.png", "wb") as f:
        shutil.copyfileobj(image_data.raw, f) 


def speedup_audio(path):
    sound = AudioSegment.from_file(path)
    new_sound = sound._spawn(sound.raw_data, overrides = {
        "frame_rate": int(sound.frame_rate * 1.2)
    })

    return new_sound.set_frame_rate(sound.frame_rate)


def create_video(audio, image, output_name, fps):
    clip = mpe.VideoFileClip(image)
    background_audio = mpe.AudioFileClip(audio)
    final_clip = clip.set_audio(background_audio)
    final_clip.write_videofile(output_name, fps=fps)

max_results = 10
results = YoutubeSearch(sys.argv[1], max_results=max_results).to_json()
url_suffix = json.loads(results)["videos"][random.randint(0, max_results - 1)]["url_suffix"]

get_random_image()

try:
    download_video("https://youtube.com" + url_suffix)
except Exception as e:
    print("error: " + e)
    print("Try running the script again")
    sys.exit(1)

nightcore = speedup_audio("audio.mp3")
nightcore.export("fast.mp3", format="mp3")

create_video("fast.mp3", "image.png", "nightcore.mp4", 1)

os.remove("audio.mp3")
os.remove("image.png")
os.remove("fast.mp3")

print("\n\noriginal url: https://youtube.com" + url_suffix)

