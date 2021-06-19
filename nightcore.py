from __future__ import unicode_literals
import youtube_dl
import requests
from xml.etree import ElementTree
import random
from bs4 import BeautifulSoup
import shutil

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
    image_number = random.randint(0, 1000)
    url = f"https://safebooru.org/index.php?page=post&s=view&id={image_number}"

    data = requests.get(url).content
    soup = BeautifulSoup(data, "html.parser")
    image_url = soup.find(id="image")['src']
    
    image_data = requests.get(image_url, stream=True)

    with open("image.png", "wb") as f:
        shutil.copyfileobj(image_data.raw, f) 


get_random_image()
download_video("https://www.youtube.com/watch?v=9lNZ_Rnr7Jc")
