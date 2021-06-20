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


def get_random_image_new():
    tag = random.choice(["1girl", "2girls", "looking_at_another", "vocaloid"])
    url = f"https://safebooru.org/index.php?page=post&s=list&tags=width:1920+height:1080+{tag}"
    page = requests.get(url).content

    soup = BeautifulSoup(page, "html.parser")
    last = soup.find(alt="last page")
    url = "https://safebooru.org/index.php" + last["href"]

    data = requests.get(url).content
    soup = BeautifulSoup(data, "html.parser")
    
    content = soup.find(class_="content")
    thumbnails = content.find_all(class_="thumb")
    thumbnail = random.choice(thumbnails)

    link = thumbnail.find("a")["href"]
    actual_page = requests.get("https://safebooru.org/" + link).content

    soup = BeautifulSoup(actual_page, "html.parser")
    image = soup.find(id="image")

    image_data = requests.get(image["src"], stream=True)

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

def get_music_video_link(videos, max_results):
    global download_from_link

    if not download_from_link:
        while True: 
            index = random.randint(0, max_results - 1)
            print(videos[index]["duration"])
            
            if len(videos[index]["duration"].split(':')) >= 3:
                continue

            if len(videos[index]["duration"].split(':')[0]) >= 2:
                print("Looking for another video...")
                continue
            
            print("found video below ten minutes with a duration of " + videos[index]["duration"])
            return videos[index]["url_suffix"]


print("\n\nSearching for " + sys.argv[1] + "\n\n")

download_from_link = sys.argv[1].startswith("https://www.youtube.com/watch") or sys.argv[1].startswith("https://youtube.com/watch")

max_results = 20 
results = YoutubeSearch(sys.argv[1], max_results=max_results).to_json()
videos = json.loads(results)["videos"]
max_results = len(videos) - 1

if max_results < 0:
    if not download_from_link:
        print("Couldnt find any videos; try again")
        sys.exit(1)


url_suffix = ""

if not download_from_link:
    url_suffix = get_music_video_link(videos, max_results)
    print("found video: https://youtube.com" + url_suffix)

get_random_image_new()

while True:
    try:
        if download_from_link:
            print("Downloading from url")
            download_video(sys.argv[1])
        else:
            print("Not downloading from url")
            download_video("https://youtube.com" + url_suffix)

        break
    except:
        if not download_from_link:
            url_suffix = get_music_video_link(videos, max_results)

        print("error downloading video, trying again...")
        continue

nightcore = speedup_audio("audio.mp3")
nightcore.export("fast.mp3", format="mp3")

create_video("fast.mp3", "image.png", "nightcore.mp4", 1)

os.remove("audio.mp3")
os.remove("image.png")
os.remove("fast.mp3")

print("\n\noriginal video url: https://youtube.com" + url_suffix)

