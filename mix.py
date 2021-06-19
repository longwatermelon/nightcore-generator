import os
import sys
import moviepy.editor as mpe

if os.path.exists("mix.mp4"):
    os.remove("mix.mp4")

for term in sys.argv[1:]:
    print(f"Creating nightcore video '{term}'")
    os.system(f"/usr/bin/python3 nightcore.py \"{term}\"")

    if os.path.exists("mix.mp4"):
        mix = mpe.VideoFileClip("mix.mp4")
        clip = mpe.VideoFileClip("nightcore.mp4")
        final_clip = mpe.concatenate_videoclips([mix, clip])
        
        os.remove("mix.mp4")
        final_clip.write_videofile("mix.mp4")
        os.remove("nightcore.mp4")
    else:
        os.rename("nightcore.mp4", "mix.mp4")
