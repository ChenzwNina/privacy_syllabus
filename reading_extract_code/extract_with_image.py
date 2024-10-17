# This is the main function to call.
import json
import pandas as pd
import pdb
import os
from Functions.judge_url_type import get_content_and_url
from Functions.send_screenshots_to_API import send_images
from Functions.api_result_process import process_first_api_result, process_second_api_result, empty_content
from Functions.send_text_readings_to_API import text_reading_sent_message

# Path to image folder
class_folder = "/Users/ninachen/Desktop/extract_with_images"

# Get this information from spreadsheet
spreeadsheet_path = "/Users/ninachen/Desktop/Class_Reading_Mapping.xlsx"
df_original = pd.read_excel(spreeadsheet_path)

# Select class number
select_class_number = 125

# How many images sent to API at the same time
batch_size = 3

# Get url and class id
class_id = df_original["Class ID"][select_class_number-1]
cell_url = df_original["Links"][select_class_number-1]

# If the url cell has multiple url, send each for processing
if ", " in cell_url:
    separate_url_list = cell_url.split(", ")
else:
    separate_url_list = [cell_url]

count = 0
final_tokens = 0

for url in separate_url_list:

    # Create a class folder if it does not exist
    folder_path = f"{class_folder}/{class_id}"
    os.makedirs(folder_path, exist_ok = True)
    print(f'folder path: {class_folder}/{class_id}')

    # Get syllabus content with embedded url and url mapping, also take screenshots under the same folder.
    syllabus_content, url_mappings, reason = get_content_and_url(url, class_folder, class_id)

    pdb.set_trace()

    # Get extraction by sending the screenshots into API
    temp_results, tokens1 = send_images(class_folder, class_id, batch_size)

    # Process initial API results
    df = process_first_api_result(temp_results, class_folder, class_id)

    # Send the reading and extracted text with url abbrev to API.
    results_with_url, tokens2 = text_reading_sent_message(df, syllabus_content)

    if results_with_url == None:
        # Count tokens used in first API
        print(f"No reading identified. The first API uses {tokens1} tokens.")

        empty_content(class_folder, class_id)


    else:
        # Replace url abbreviation with actual url from url mapping. Download the final reading spreadsheet under the class folder.
        process_second_api_result(results_with_url, url_mappings, class_folder, class_id, df)

        count += 1
        
        class_id = f"{class_id}_{count}"

        each_url_tokens = tokens1 + tokens2

        final_tokens += each_url_tokens 

        # Count total tokens used in two API
        print(f"[Image] The syllabus costs {final_tokens} tokens")

