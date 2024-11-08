import pdb
import os
import pandas as pd
from Functions.judge_url_type_no_screenshot import get_content_and_url
from Functions.send_text_only_to_api import api_syllabus_classification
from Functions.export_reading_syllabus import export_reading_syllabus

def extract_with_text(spreadsheet_path, select_class_number, max_words):
    
    # Get this information from spreadsheet
    df_original = pd.read_excel(spreadsheet_path)

    # Path to downloaded PDF.
    class_folder = "/Users/ninachen/Desktop/reading_extractions"
    
    # If you are testing with text without chunks, create a new folder
    # else:
    #     class_folder = "/Users/ninachen/Desktop/extract_with_text"

    # Find url information
    result = df_original[df_original["Class ID"] == select_class_number]
    class_id = select_class_number
    cell_url = result["Links"].values[0]

    print(f"Syllabus URL {cell_url}")

    # If the url cell has multiple url, send each for processing
    if ", " in cell_url:
        separate_url_list = cell_url.split(", ")
    else:
        separate_url_list = [cell_url]

    count = 0
    final_prompt_token = 0
    final_completion_token = 0

    for url in separate_url_list:

        # Create a class folder if it does not exist
        folder_path = f"{class_folder}/{class_id}"
        os.makedirs(folder_path, exist_ok = True)
        print(f'folder path: {class_folder}/{class_id}')

        # Get syllabus content and url mappings.
        syllabus_with_url, syllabus_url_mappings, reason = get_content_and_url(url, class_folder, class_id)

        if syllabus_with_url == "error":
            raise Exception("A general error occurred with the syllabus URL.")

        # Run reading extraction API.
        syllabus_reading_list, chunk_number, text_prompt_token_single, text_completion_token_single = api_syllabus_classification(syllabus_with_url, max_words)

        # Export reading extraction into a spreadsheet
        export_reading_syllabus(syllabus_reading_list, class_id, class_folder, syllabus_url_mappings, chunk_number)

        count += 1
        
        class_id = f"{class_id}_{count}"

        final_prompt_token += text_prompt_token_single
        final_completion_token += text_completion_token_single

    # Count total tokens used in two API
    print(f"[Text] The syllabus costs {final_prompt_token} prompt tokens")
    print(f"[Text] The syllabus costs {final_completion_token} completion tokens")

    return final_prompt_token, final_completion_token