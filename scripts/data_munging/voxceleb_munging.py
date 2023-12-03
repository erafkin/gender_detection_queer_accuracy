"""
    Author: Emma Rafkin
    Script to download the selected youtube clips and munge them from VoxCeleb for the queer and control set of celebrities.
"""
import os
from pytube import YouTube
from pydub import AudioSegment
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
import subprocess

f = open("./resources/straight_voices.txt", "r")
queers = f.readlines()
for queer in queers:
    vox_id, name, gender, vox_dataset, split = queer.split()
    path = f"./data/{vox_dataset}_{split}/{vox_id}"
    youtube_ids = os.listdir(path)
    youtube_ids = [y for y in youtube_ids if y != ".DS_Store"]
    videos = [f"http://www.youtube.com/watch?v={yt_id}" for yt_id in youtube_ids]

    if len(videos) >= 3:
        n = 3
    else:
        n = len(videos)
    for yt_id in youtube_ids[0:n]:
        try:
            yt=YouTube(f"http://www.youtube.com/watch?v={yt_id}")
            t=yt.streams.filter(only_audio=True).all()
            fps = yt.streams.filter(mime_type="video/mp4")[0].fps
            t[0].download(output_path=f"data/straight_full_videos/{vox_id}/{yt_id}")
            filename = os.listdir(f"data/straight_full_videos/{vox_id}/{yt_id}")[0]
            os.rename(f"data/straight_full_videos/{vox_id}/{yt_id}/{filename}", f"data/straight_full_videos/{vox_id}/{yt_id}/{yt_id}.mp4")
            filename=yt_id
            subprocess.run(f"ffmpeg -i data/straight_full_videos/{vox_id}/{yt_id}/{filename}.mp4 {filename}.wav",shell=True)
            os.rename(f"{filename}.wav", f"data/straight_full_videos/{vox_id}/{yt_id}/{filename}.wav")
            os.remove(f"data/straight_full_videos/{vox_id}/{yt_id}/{filename}.mp4")
        except Exception as e:
            print('youtube video failed:')
            print(yt_id)
            print(e)
        # user_path = f"./data/{vox_dataset}_{split}/{vox_id}/{yt_id}"
        # for clip in os.listdir(user_path):
        #     f2 = open(f"./data/{vox_dataset}_{split}/{vox_id}/{yt_id}/{clip}", "r")
        #     lines = f2.read()
        #     lines = lines.split("\n")
        #     lines = [l.strip() for l in lines if not l == ""]
        #     f2.close()

        #     idx_start = 0
        #     idx_end = len(lines) - 2
        #     for idx, line in enumerate(lines):
              
        #         if line.split()[0] == "FRAME":
        #             idx_start = idx + 1
        #             break
        #     start_frame = int(lines[idx_start].split()[0])
        #     end_frame = int(lines[idx_end].split()[0])
        #     print(f"fps: {fps}")
        #     t1 = int(start_frame / fps)  # Works in milliseconds
        #     t2 = int(end_frame / fps) 
        #     print(t1)
        #     print(t2)
        #     subprocess.run(f"ffmpeg -i data/straight_full_videos/{vox_id}/{yt_id}/{filename}.wav -map 0 -acodec copy -ss {t1} -to {t2} data/straight_full_videos/{vox_id}/{yt_id}/{int(clip.split('.')[0])}.wav", shell=True)

            # newAudio = AudioSegment.from_wav(f"data/straight_full_videos/{vox_id}/{yt_id}/{filename}.wav")
            # newAudio = newAudio[t1:t2]
            # newAudio.export(f"data/straight_full_videos/{vox_id}/{yt_id}/{int(clip.split('.')[0])}.wav", format="wav") #Exports to a wav file in the current path.


    
