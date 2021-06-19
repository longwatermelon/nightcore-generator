from __future__ import unicode_literals
import youtube_dl
import requests
from xml.etree import ElementTree
import random
from bs4 import BeautifulSoup
import shutil
from pydub import AudioSegment
import moviepy.editor as mpe
import sys


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
        "frame_rate": int(sound.frame_rate * 1.25)
    })

    return new_sound.set_frame_rate(sound.frame_rate)


def create_video(audio, image, output_name, fps):
    clip = mpe.VideoFileClip(image)
    background_audio = mpe.AudioFileClip(audio)
    final_clip = clip.set_audio(background_audio)
    final_clip.write_videofile(output_name, fps=fps)

get_random_image()
download_video("https://www.youtube.com/watch?v=9lNZ_Rnr7Jc")

nightcore = speedup_audio("audio.mp3")
nightcore.export("nightcore.mp3", format="mp3")

create_video("audio.mp3", "image.png", "final_video.mp4", 1)

