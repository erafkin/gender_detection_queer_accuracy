"""
    Author: Emma Rafkin
    Script to download the selected youtube clips and munge them from VoxCeleb for the queer and control set of celebrities.
"""
import os
# import youtube_dl as ydl
from pytube import YouTube
from pydub import AudioSegment
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
import subprocess
import ffmpeg



f = open("./resources/queer_voices.txt", "r")
queers = f.readlines()
for queer in queers[0:1]:
    vox_id, name, gender, vox_dataset, split = queer.split()
    path = f"./data/{vox_dataset}_{split}/{vox_id}"
    youtube_ids = os.listdir(path)
    videos = [f"http://www.youtube.com/watch?v={yt_id}" for yt_id in youtube_ids]
    for yt_id in youtube_ids:
        yt=YouTube(f"http://www.youtube.com/watch?v={yt_id}")
        t=yt.streams.filter(only_audio=True).all()
        t[0].download(output_path=f"data/voxceleb_full_videos/{yt_id}")
        filename = os.listdir(f"data/voxceleb_full_videos/{yt_id}")[0]
        # print(filename)
        # print(filename[:-4])
        # print(filename[:-4] + ".mp3")
        # _ = (
        #     ffmpeg
        #     .input(filename)
        #     .output(filename[:-4] + ".mp3")
        #     .run()
        # )
        subprocess.run(f"ffmpeg -i data/voxceleb_full_videos/{yt_id}/{filename}.mp4 .data/voxceleb_full_videos/{yt_id}/{filename}.mp3",shell=True)
        stream = yt.streams.filter(progressive=True)[0]
        print("fps: " + str(stream.fps))
        fps = stream.fps
        user_path = f"./data/{vox_dataset}_{split}/{vox_id}/{yt_id}"
        for clip in os.listdir(user_path):
            f2 = open(f"./data/{vox_dataset}_{split}/{vox_id}/{yt_id}/{clip}", "r")
            lines = f2.read()
            lines = lines.split("\n")
            lines = [l.strip() for l in lines if not l == ""]


            # print(lines)
            idx_start = 0
            idx_end = len(lines) -2
            for idx, line in enumerate(lines):
                # print(line)
                # print(line.split())
                if line.split()[0] == "FRAME":
                    idx_start = idx + 1
                    break
            start_frame = int(lines[idx_start].split()[0])
            end_frame = int(lines[idx_end].split()[0])
   
            t1 = fps* start_frame * 1000  # Works in milliseconds
            t2 = fps * end_frame * 1000
            print(t1)
            print(t2)
            newAudio = AudioSegment.from_mp3(f"data/voxceleb_full_videos/{yt_id}/{filename}")
            newAudio = newAudio[t1:t2]
            newAudio.export("data/voxceleb_full_videos/{yt_id}/{filename}", format="wav") #Exports to a wav file in the current path.



    
