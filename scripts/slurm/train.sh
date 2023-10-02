#!/bin/bash
#SBATCH --job-name="emma_train_classifier"
#SBATCH --output="%x.o%j"
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --time=03:00:00
#SBATCH --mem=3G
#SBATCH --mail-user=epr41@georgetown.edu
#SBATCH --mail-type=END,FAIL

module load cuda/11.8
module load python3/3.6.8
python3 -m venv venv
source venv/bin/activate
which python3
pip3 install -r requirements.txt
pip3 show datasets
python3 ./scripts/train.py
