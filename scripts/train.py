"""
    Author: Emma Rafkin

    Heavily following this tutorial: https://huggingface.co/docs/transformers/tasks/audio_classification
    and loading in data using huggingface: https://huggingface.co/docs/datasets/audio_dataset

"""

from datasets import load_dataset, Audio
from transformers import AutoFeatureExtractor
import scripts.evaluate_queer_voices as evaluate_queer_voices
import numpy as np
from transformers import AutoModelForAudioClassification, TrainingArguments, Trainer
import os

# Load the dataset and split it for training and validation in training
commonvoice = load_dataset("audiofolder", data_dir=f"{os.getcwd()}/data/commonvoice")
commonvoice = commonvoice["train"].train_test_split()
print("Training Dataset, train-test split")
print(commonvoice)
# resample the audio to work with wav2vec2
commonvoice = commonvoice.cast_column("audio", Audio(sampling_rate=16000)) 
# Get the labels out of the dataset so we remember what they are

## Labels:
## should be: {'0': 'men', '1': 'other', '2': 'women'}
labels = commonvoice["train"].features["label"].names
label2id, id2label = dict(), dict()
for i, label in enumerate(labels):
    label2id[label] = str(i)
    id2label[str(i)] = label
print("labels")
print(id2label)

# This will pull out the features
feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base")

# This loads the audio file (resamples if necessary but it isnt), checks that its the right sampling rate, and truncates/batches it if necessary
def preprocess_function(examples):
    audio_arrays = [x["array"] for x in examples["audio"]]
    inputs = feature_extractor(
        audio_arrays, sampling_rate=feature_extractor.sampling_rate, max_length=16000, truncation=True
    )
    return inputs

encoded_dataset = commonvoice.map(preprocess_function, remove_columns="audio", batched=True)
accuracy = evaluate_queer_voices.load("accuracy")
def compute_metrics(eval_pred):
    predictions = np.argmax(eval_pred.predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=eval_pred.label_ids)

# set up trainer
num_labels = len(id2label)
model = AutoModelForAudioClassification.from_pretrained(
    "facebook/wav2vec2-base", num_labels=num_labels, label2id=label2id, id2label=id2label
)

training_args = TrainingArguments(
    output_dir="gender_classifier_20_epochs",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=32,
    gradient_accumulation_steps=4,
    per_device_eval_batch_size=32,
    num_train_epochs=20,
    warmup_ratio=0.1,
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    push_to_hub=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset["train"],
    eval_dataset=encoded_dataset["test"],
    tokenizer=feature_extractor,
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.save_model("gender_classifier_20_epochs")
