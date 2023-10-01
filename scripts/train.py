"""
    Author: Emma Rafkin

    Heavily following this tutorial: https://huggingface.co/docs/transformers/tasks/audio_classification
    and loading in data using huggingface: https://huggingface.co/docs/datasets/audio_dataset

"""

from datasets import load_dataset
dataset = load_dataset("audiofolder", data_dir="/Users/erafkin/Desktop/Desktop/2023-2024/fall/signal_processing/gender_detection_queer_accuracy/data/commonvoice")
## Labels:
## men: 0, other: 1, women: 2
