#!/bin/bash
#SBATCH --job-name="emma_evaluate_classifier"
#SBATCH --nodes=1
#SBATCH --output="%x.o%j"
#SBATCH --gres=gpu:1
#SBATCH --mem=8G
#SBATCH --mail-user=epr41@georgetown.edu
#SBATCH --mail-type=END,FAIL

module load cuda/11.8
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 ./scripts/evaluate_classifier.py

