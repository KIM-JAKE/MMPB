import json
import csv
import os
import random
from collections import defaultdict
import numpy as np

def load_json(json_file):
    """Load JSON data from a given file."""
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def shuffle_choices(details):
    """Shuffle answer choices and update the correct answer index."""
    choices = [details.get("A", ""), details.get("B", ""), details.get("C", ""), details.get("D", "")]
    correct_answer_text = choices["ABCD".index(details["Answer"])] if "Answer" in details and details["Answer"] in "ABCD" else ""
    
    random.shuffle(choices)
    
    new_answer = "ABCD"[choices.index(correct_answer_text)] if correct_answer_text else ""
    
    return choices, new_answer

PARAPHRASES = [
    "Does this image connect to <sks>'s positive or negative preferences? Answer with Yes or No.",
    "Is the content of this image associated with <sks>'s likes or dislikes? Answer with either Yes or No.",
    "Does this image pertain to <sks>'s favorable or unfavorable inclinations? Please answer Yes or No.",
    "Is this image connected to what  <sks> prefers or dislikes? Answer Yes or No.",
    "Is the image linked to <sks>'s positive or negative taste? Answer with either Yes or No.",
    "Does this picture relate to <sks>'s positive or negative leanings? Please respond with Yes or No.",
    "Does this image correlate with <sks>'s positive or negative orientation? Answer with either Yes or No.",
    "Is the image reflective of <sks>'s positive or negative preference? Please reply with Yes or No.",
    "Is the image tied to <sks>’s positive or negative liking? Respond with either Yes or No.",
    "Does this image correlate with <sks>'s positive or negative preference? Answer with either Yes or No.",
]

NEGATIVE_PARAPHRASES = [
    "Is this image not connected to <sks>'s positive or negative preferences? Answer with Yes or No.",
    "Is the content of this image not associated with <sks>'s likes or dislikes? Answer with either Yes or No.",
    "Does this image not pertain to <sks>'s favorable or unfavorable inclinations? Please answer Yes or No.",
    "Is this image not connected to what <sks> prefers or dislikes? Answer Yes or No.",
    "Is the image not linked to <sks>'s positive or negative taste? Answer with either Yes or No.",
    "Does this picture not relate to <sks>'s positive or negative leanings? Please respond with Yes or No.",
    "Does this image not correlate with <sks>'s positive or negative orientation? Answer with either Yes or No.",
    "Is the image not reflective of <sks>'s positive or negative preference? Please reply with Yes or No.",
    "Is the image not tied to <sks>’s positive or negative liking? Respond with either Yes or No.",
    "Does this image not correlate with <sks>'s positive or negative preference? Answer with either Yes or No.",
]

BASE_QUERY = "Is this image related to <sks>'s positive or negative preference? Answer with either ‘Yes’ or ‘No’."

def process_json_data(data, human_name, attribute, category, l2_category, preferences, descriptions, index):
    """Process JSON data and return formatted rows."""
    rows = []
    preference_prompt = preferences.get(human_name, "Unknown preferences")
    description_simple_prompt = next((desc["description"] for desc in descriptions['simple'] if desc["person"] == human_name), "Unknown description")
    description_moderate_prompt = next((desc["description"] for desc in descriptions['moderate'] if desc["person"] == human_name), "Unknown description")
    description_detailed_prompt = next((desc["description"] for desc in descriptions['detailed'] if desc["person"] == human_name), "Unknown description")
        
    # prompt = description_prompt + preference_prompt
    
    if data:
        iterable = data.items() if category == "preference" else [(None, data)]
        for concept, images in iterable:
            for image_path, queries in images.items():
                if isinstance(queries, list):  
                    for details in queries:
                        # 만약 Query가 BASE_QUERY와 같다면 paraphrasing 진행
                        if details.get("Query", "") == BASE_QUERY:
                            if random.choice([True, False]):
                                details["Query"] = random.choice(NEGATIVE_PARAPHRASES)
                                if l2_category == "awareness":
                                    details["Answer"] = "No"
                                elif l2_category == "overconcept":
                                    details["Answer"] = "Yes"
                                else:
                                    details["Answer"] = details.get("Answer", "")
                            else:
                                details["Query"] = random.choice(PARAPHRASES)
                        row = [
                            index,  # index
                            details["Query"],  # question
                            "", "", "", "",  # Empty choices for recognition, awareness, and overconcept
                            image_path.lstrip("./"),  # image_path
                            details.get("Answer", ""),  # answer
                            attribute,  # attribute
                            category,  # category
                            l2_category,  # l2-category
                            concept if category == "preference" else "",  # concept for preference
                            details.get("Target", ""),
                            human_name,  # name
                            preference_prompt,  # prompt
                            description_simple_prompt,
                            description_moderate_prompt,
                            description_detailed_prompt
                        ]
                        rows.append(row)
                        index += 1
                else:  
                    if l2_category == "inconsistency":
                        shuffled_choices, new_answer = shuffle_choices(queries)
                    else:
                        shuffled_choices = ["", "", "", ""]
                        new_answer = queries.get("Answer", "")
                    
                    if queries.get("Query", "") == BASE_QUERY:
                        if random.choice([True, False]):
                            queries["Query"] = random.choice(NEGATIVE_PARAPHRASES)
                            if l2_category == "awareness":
                                new_answer = "No"
                            elif l2_category == "overconcept":
                                new_answer = "Yes"
                            else:
                                new_answer = queries.get("Answer", "")
                        else:
                            queries["Query"] = random.choice(PARAPHRASES)
                    
                    row = [
                        index,  # index
                        queries["Query"],  # question
                        shuffled_choices[0],  # choice A
                        shuffled_choices[1],  # choice B
                        shuffled_choices[2],  # choice C
                        shuffled_choices[3],  # choice D
                        image_path.lstrip("./"),  # image_path
                        new_answer,  # answer
                        attribute,  # attribute
                        category,  # category
                        l2_category,  # l2-category
                        concept if category == "preference" else "",  # concept for preference
                        queries.get('Target', ""),
                        human_name,  # name
                        preference_prompt,  # prompt
                        description_simple_prompt,
                        description_moderate_prompt,
                        description_detailed_prompt
                    ]
                    rows.append(row)
                    index += 1
    return rows, index

def json_to_csv(base_path, preferences_file, descriptions_file, csv_file):
    """Convert multiple JSON files into a single CSV file."""
    headers = ["index", "question", "A", "B", "C", "D", "image_path", "answer", "attribute", "category", "l2-category", "concept", "target", "name", "preference", "description_simple", "description_moderate", "description_detailed"]
    rows = []
    index = 1
    
    # Load human preferences and descriptions
    preferences = load_json(preferences_file) or {}
    descriptions = load_json(descriptions_file) or {}
    
    attributes = ["human", "animal", "character", "object"]
    categories = ["preference", "recognition"]
    l2_categories = ["awareness", "inconsistency", "overconcept"]
    
    for attribute in attributes:
        attribute_folder = os.path.join(base_path, attribute, "test")
        if not os.path.exists(attribute_folder):
            continue
        
        for human_name in os.listdir(attribute_folder):
            human_folder = os.path.join(attribute_folder, human_name)
            
            for category in categories:
                category_folder = os.path.join(human_folder, category)
                if not os.path.exists(category_folder):
                    continue
                
                for l2_category in l2_categories:
                    json_file = os.path.join(category_folder, f"{l2_category}.json")
                    data = load_json(json_file)
                    processed_rows, index = process_json_data(data, human_name, attribute, category, l2_category, preferences, descriptions, index)
                    rows.extend(processed_rows)
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    
    print(f"CSV file saved: {csv_file}")

# Example usage
base_path = "/workspace/MMPB"
preferences_file = "/workspace/MMPB/human/formatted_preferences_full.json"
descriptions_file = "/workspace/MMPB/formatted_descriptions_full.json"
csv_file = "/workspace/MMPB/dataset3.csv"
json_to_csv(base_path, preferences_file, descriptions_file, csv_file)