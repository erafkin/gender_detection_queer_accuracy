# Accuracy of Gender Detection of Queer Voices
Signal Processing final project. I built a gender classifier using CommonVoice data and tested it against queer voices (known celebrities, pulling clips listed in VoxCeleb 1 and 2)

## Environment
Built using Python 3.10. To run on a Mac:
- `python3.10 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

This was also tested and run in Python 3.6 because that is what the HPC had.

The models were trained on the Georgetown Google HPC, there are slurm scripts [here](scripts/slurm/) if you are curious about what resources were used or if you want to replicate it.

## Data
I have chosen to not upload the data here, as for CommonVoice sometimes users pull their voices and the VoxCeleb data is no longer available on their website directly, just the identifiers. I will just list what data I used and where I got it
- Training: [Common Voice Delta Segment 10.0](https://commonvoice.mozilla.org/en/datasets)
- Evaluation: VoxCeleb 1 and 2. 
    - Speaker ID, youtube file name, and frames of speech found [here](https://mm.kaist.ac.kr/datasets/voxceleb/index.html)
    - Metadata found (here)[https://www.openslr.org/49/]
    - Lists of people that were used for the evalation is under the [resources folder](resources/)

Data munging scripts can be found [here](scripts/data_munging).
- For commonvoice, the data was filtered to only include clips that were validated, not on the reported list, and have a labeled gender. They were then organized into seperate folders for uploading dynamically into the training script.
- For voxceleb: *TODO*
