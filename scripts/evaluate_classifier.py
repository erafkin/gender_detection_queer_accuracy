from transformers import pipeline
from datasets import load_dataset, Audio
import os
import json

model = "tertiary_classifier_20_epochs"
classifier = pipeline("audio-classification", model=model)


"""
    need 4 folders, m s/q, f s/q
"""

dataset = load_dataset("audiofolder", data_dir=f"{os.getcwd()}/data/queer_clips")
dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))
final_results = {"men": [], "women": []}
for audio_file in dataset["train"]["audio"]:
    gender = audio_file["path"].split("/")[-2]
    result = classifier(audio_file)
    final_results[gender].append({"result": result, "name": audio_file["path"].split("/")[-1]})
with open(f"{model}_results.json", "w") as f:
    json.dump(final_results, f)
    f.close()
