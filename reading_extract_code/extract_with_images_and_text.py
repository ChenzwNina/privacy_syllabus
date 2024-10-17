import pandas as pd
import os
import pdb

from Functions.judge_url_type import get_content_and_url
from Functions.send_images_text_to_API import send_images_text
from Functions.export_image_text_syllabus import export_reading_from_image_text


# Path to image folder
class_folder = "/Users/ninachen/Desktop/extract_with_image_text"

# Get this information from spreadsheet
spreeadsheet_path = "/Users/ninachen/Desktop/Class_Reading_Mapping.xlsx"
df_original = pd.read_excel(spreeadsheet_path)

# Select class number
select_class_number = 113

# Number of images sent to API
batch_size = 5

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
    syllabus_with_url, url_mappings, reason = get_content_and_url(url, class_folder, class_id)

    pdb.set_trace()

    # Get extraction by sending the screenshots and the parsed text into API
    temp_results, each_url_tokens = send_images_text(class_folder, class_id, batch_size, syllabus_with_url)

    # Process API results.
    export_reading_from_image_text(temp_results, class_folder, class_id, url_mappings)

    final_tokens += each_url_tokens

    count += 1
    
    class_id = f"{class_id}_{count}"

# Count total tokens used in two API
print(f"[Image] The syllabus costs {final_tokens} tokens")