import os
import pandas as pd
from tqdm import tqdm 
validated_dataset = pd.read_table("./data/cv-corpus-10.0-delta-2022-07-04/en/validated.tsv", delimiter="\t")
validated_dataset = validated_dataset[validated_dataset['gender'].notna()]
reported_clips = pd.read_table("./data/cv-corpus-10.0-delta-2022-07-04/en/reported.tsv", delimiter="\t")
reported_clips = list(reported_clips["sentence"].unique())
validated_dataset = validated_dataset[~validated_dataset['sentence'].isin(reported_clips)]

print(validated_dataset["gender"].value_counts())
# NOTE:
# male      3458
# female    3212
# other      300
for index, row in tqdm(validated_dataset.iterrows()):
    if row["gender"] == "other":       
        os.rename(f"./data/cv-corpus-10.0-delta-2022-07-04/en/clips/{row['path']}", f"./data/commonvoice_train_other/{row['path']}")
