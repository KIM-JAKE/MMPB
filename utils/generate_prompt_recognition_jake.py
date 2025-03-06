import os
import json
import argparse
import pandas as pd
from PIL import Image, UnidentifiedImageError
from ovis.serve.runner import RunnerArguments, OvisRunner

parser = argparse.ArgumentParser()
parser.add_argument('--prompt_level', type=str, default="detail", choices=["simple", "moderate", "detail"],
                    help='Choose the prompt level: simple, moderate, or detail.')
args = parser.parse_args()

attribute = "object"

base_dir = f"/workspace/MMPB/{attribute}/train"

# Initialize the OvisRunner
runner_args = RunnerArguments(model_path='AIDC-AI/Ovis2-34B')
runner = OvisRunner(runner_args)

# Prompt texts for different levels
prompt_texts = {
    # Todo
    "simple": {
        "human": "Describe <sks> briefly.",
        "animal": "Describe <sks> briefly.",
        "object": "Describe <sks> briefly.",
        "character": "Describe <sks> briefly."
    },
    # Todo
    "moderate": {
        "human": "Provide a moderate description of <sks>, focusing on main features.",
        "animal": "Provide a moderate description of <sks>, focusing on main features.",
        "object": "Provide a moderate description of <sks>, focusing on main features.",
        "character": "Provide a moderate description of <sks>, focusing on main features."
    },
    "detail": {
        "human": ("Observe the person across all five images and provide a single, unified description of <sks>. "
                  "Name the person as <sks> and ensure the description uses '<sks>' naturally throughout. "
                  "Focus on consistent traits rather than describing each image separately. "
                  "Describe <sks>'s physical appearance, clothing style, and distinguishing features in a single paragraph."),
        "animal": ("Observe the animal across all five images and provide a single, unified description of <sks>. "
                   "Name the species as <sks> and ensure the description uses '<sks>' naturally throughout. "
                   "Focus on consistent traits rather than describing each image separately. "
                   "Describe <sks>'s species, physical appearance, and distinguishing features in a single paragraph."),
        "object": ("Observe the object across all five images and provide a single, unified description of <sks>. "
                   "Name the object as <sks> and ensure the description uses '<sks>' naturally throughout. "
                   "Focus on consistent traits rather than describing each image separately. "
                   "Describe <sks>'s type, physical appearance, and distinguishing features in a single paragraph."),
        "character": ("Observe the character across all five images and provide a single, unified description of <sks>. "
                      "Name the character as <sks> and ensure the description uses '<sks>' naturally throughout. "
                      "Focus on consistent traits rather than describing each image separately. "
                      "Describe <sks>'s physical appearance, outfit, and distinguishing features in a single paragraph.")
    }
}

text = prompt_texts.get(args.prompt_level, {}).get(attribute, "Unknown category")

# List to store the results
results = []
error_log = []  # Store any errors

# Iterate over each person's folder
for person in sorted(os.listdir(base_dir)):
    person_dir = os.path.join(base_dir, person)
    
    if os.path.isdir(person_dir):  # Ensure it's a directory
        images = []
        
        # Load images from 0.png to 4.png
        for i in range(5):  # Assuming 5 images per person
            image_path = os.path.join(person_dir, f"{i}.png")
            if os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    img.verify()  # Verify if it's a valid image
                    images.append(Image.open(image_path))  # Re-open for processing
                except (UnidentifiedImageError, OSError) as e:
                    error_log.append({"person": person, "image": image_path, "error": str(e)})
                    print(f"Skipping invalid image: {image_path} - {e}")

        if len(images) == 5:  # Ensure all images are available
            # Run the model inference
            response = runner.run([*images, prompt_text])
            description = response['output']
            
            # Store the results
            results.append({"person": person, "description": description})
        else:
            print(f"Skipping {person} due to missing or invalid images.")

# Save as JSON
json_output_path = f"/workspace/MMPB/{attribute}/descriptions.json"
with open(json_output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

# Save as CSV
csv_output_path = f"/workspace/MMPB/{attribute}/descriptions.csv"
df = pd.DataFrame(results)
df.to_csv(csv_output_path, index=False, encoding="utf-8")

# Save error log
error_log_path = f"/workspace/MMPB/{attribute}/error_log.json"
with open(error_log_path, "w", encoding="utf-8") as f:
    json.dump(error_log, f, indent=4, ensure_ascii=False)

print("Descriptions saved successfully.")
if error_log:
    print(f"Some images were skipped due to errors. Check {error_log_path} for details.")