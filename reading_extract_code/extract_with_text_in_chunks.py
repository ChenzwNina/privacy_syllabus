# This is the main function to call other functions

import os
import pandas as pd
from Functions.judge_url_type_no_screenshot import get_content_and_url
from Functions.send_text_only_to_api import api_syllabus_classification
from Functions.export_reading_syllabus import export_reading_syllabus


# Get this information from spreadsheet
spreeadsheet_path = "/Users/ninachen/Desktop/Class_Reading_Mapping.xlsx"
df_original = pd.read_excel(spreeadsheet_path)

# Select class number
select_class_number = 125

# Set the maximum characters as a chunk for API to process at one time.
max_words = 1000000

if max_words == 1000:
    # Path to downloaded PDF.
    class_folder = "/Users/ninachen/Desktop/extract_with_text_chunks_1000"
else:
    class_folder = "/Users/ninachen/Desktop/extract_with_text_1000"

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

    # Get syllabus content and url mappings.
    syllabus_with_url, syllabus_url_mappings, reason = get_content_and_url(url, class_folder, class_id)
            
    # Run reading extraction API.
    syllabus_reading_list, chunk_number, each_url_tokens = api_syllabus_classification(syllabus_with_url, max_words)
                    
    # Export reading extraction into a spreadsheet
    export_reading_syllabus(syllabus_reading_list, class_id, class_folder, syllabus_url_mappings, chunk_number)

    count += 1
    
    class_id = f"{class_id}_{count}"

    final_tokens += each_url_tokens 

# Count total tokens used in two API
print(f"The syllabus costs {final_tokens} tokens")