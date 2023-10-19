"""
    Author: Emma Rafkin
    Script to download the selected youtube clips and munge them from VoxCeleb for the queer and control set of celebrities.
"""
import os

f = open("./resources/queer_voices.txt", "r")
queers = f.readlines()
for queer in queers:
    vox_id, name, gender, vox_dataset, split = queer.split()
    path = f"./data/{vox_dataset}_{split}/{vox_id}"
    youtube_ids = os.listdir(path)


    
