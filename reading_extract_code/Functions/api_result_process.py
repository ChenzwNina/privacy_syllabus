# The code in this file cleans the output from first API and save a spreadsheet with reading info (url missing).
import pandas as pd
import json
import pdb

def process_first_api_result(temp_results, class_folder, class_id):

    # Get all readings in one list
    final_results = []
    total_list_number = len(temp_results)


    for item in range(total_list_number):
        if temp_results[item]is None:
            print("Found a NoneType object.")
        else:
            temp_list = json.loads(temp_results[item].replace("```json", "").replace("```", ""))

        num_empty = 0

        # See if output format is dict or a list containing dict.
        if isinstance(temp_list, dict):
            value_list = temp_list.values()
            for sig_value in value_list:
                if sig_value == '':
                    num_empty += 1
            if num_empty == len(value_list):
                continue
            else:
                final_results.append(temp_list)
        else:
            for reading in temp_list:
                value_list = reading.values()
                for sig_value in value_list:
                    if sig_value == '':
                        num_empty += 1
                if num_empty == len(value_list):
                    continue
                else:
                    final_results.append(reading)

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(final_results)

    # Save the DataFrame as a spreadsheet file
    file_path = f'{class_folder}/{class_id}/{class_id}_readings_original.xlsx'
    df.to_excel(file_path, index=False) 

    return df


def process_second_api_result(results_with_url, syllabus_url_mappings, class_folder, class_id, df):

    clean_results_with_url = json.loads(results_with_url.replace("```json", "").replace("```", ""))
    df_formatted = pd.DataFrame(clean_results_with_url)
    url_set = df_formatted['URL']
    reading_set = df_formatted['Reading Name']

    symbol = ""
    updated_url = ""

    for index, url_individual in enumerate(url_set):
        individual_reading_name = reading_set[index]

        # If there are multiple url in the cell, replace each of them.
        if "," in url_individual:
            split_url = url_individual.replace(" ", "").split(',')
            for split_item in split_url:
                true_url = syllabus_url_mappings.get(split_item)
                updated_url = updated_url + symbol + true_url
                symbol  = ", "
            df.loc[df['Reading Name'] == individual_reading_name, 'URL'] = updated_url
        else:
            true_url = syllabus_url_mappings.get(url_individual)
            df.loc[df['Reading Name'] == individual_reading_name, 'URL'] = true_url
    
    df.to_excel(f'{class_folder}/{class_id}/{class_id}_readings_final.xlsx', index = False)


def empty_content(class_folder, class_id):
    data = {
    "Reading Name": [""],
    "Author Name": [""],
    "Published Year": [""],
    "Page Numbers to Read": [""],
    "URL": [""]
    }

    # Create a DataFrame
    df_empty = pd.DataFrame(data)

    # Export the DataFrame to an Excel file
    df_empty.to_excel(f'{class_folder}/{class_id}/{class_id}_readings_final.xlsx', index = False)