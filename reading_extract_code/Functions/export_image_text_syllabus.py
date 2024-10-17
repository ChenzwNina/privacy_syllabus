import pdb
import pandas as pd
import json
import re


def export_reading_from_image_text(temp_results, class_folder, class_id, url_mappings):
    final_results = []

    pdb.set_trace()

    for i in temp_results:
        match = re.search(r'```json(.*?)```', i, re.DOTALL)
        if match:
            matched_text = match.group(1).strip()
            cleaned = json.loads(matched_text.replace("```json", "").replace("```", ""))
        else:
            print("------------format processing error------------")


        for t in cleaned:
            final_results.append(t)
    
    df = pd.DataFrame(final_results)

    # Replace URL abbreviations with actual URLs from the url_mappings dictionary, handling multiple URLs
    df['URL'] = df['URL'].apply(lambda x: ', '.join([url_mappings.get(url.strip(), url.strip()) for url in x.split(',')]))

    # Remove duplicate readings based on 'Reading Name' column
    df = df.drop_duplicates(subset=['Reading Name'])
    
    # Save to an Excel spreadsheet
    output_file = f"{class_folder}/{class_id}/{class_id}_readings.xlsx"
    df.to_excel(output_file, index=False)
