import os
import json
import pandas as pd
from PIL import Image, UnidentifiedImageError
from ovis.serve.runner import RunnerArguments, OvisRunner

runner_args = RunnerArguments(model_path='AIDC-AI/Ovis2-34B')
runner = OvisRunner(runner_args)

name = "Minjae"

# Load multiple images
image1 = Image.open(f'/workspace/MMPB/human/train/{name}/0.png')
image2 = Image.open(f'/workspace/MMPB/human/train/{name}/1.png')
image3 = Image.open(f'/workspace/MMPB/human/train/{name}/2.png')
image4 = Image.open(f'/workspace/MMPB/human/train/{name}/3.png')
image5 = Image.open(f'/workspace/MMPB/human/train/{name}/4.png')

# Text prompt
text = "Observe the person across all five images and provide a single, unified description of <sks>. Name the person as <sks> and ensure the description uses '<sks>' naturally throughout. Focus on consistent traits rather than describing each image separately. Describe <sks>'s physical appearance, clothing style, and distinguishing features in a single paragraph."

# Run inference with multiple images
response = runner.run([image1, image2, image3, image4, image5, text, general..., image, query])

print(response['output'])
<image>
