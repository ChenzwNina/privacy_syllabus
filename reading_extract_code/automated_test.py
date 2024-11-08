import os
import pandas as pd
import pdb
from extract_with_image import extract_with_image
from extract_with_images_and_text import extract_with_images_text
from extract_with_text_in_chunks import extract_with_text

# Input path of class mapping excel
class_file = "/Users/ninachen/Desktop/Class_Reading_Mapping_error 2.0.xlsx"

# Output path of token file
filename = "/Users/ninachen/Desktop/test_tokens_11.7.xlsx"

# Output path of error file
error_file = "/Users/ninachen/Desktop/error_file_11.7.xlsx"

# Process in chunks of 5 rows
skip_rows = 0

chunk_size = 5

# Read excel header
header = pd.read_excel(class_file, nrows=0).columns.tolist()

while True:

    # Read excel in chunks of chunk_size
    df_chunk = pd.read_excel(class_file, skiprows = skip_rows, nrows = chunk_size)
    
    # Break the loop if no more data is found
    if df_chunk.empty:
        break

    # Assign header to chunk
    df_chunk.columns = header

    # Get class id list of the chunk
    class_id_chunk = df_chunk["Class ID"]

    links_chunk = df_chunk["Links"]

    # Create empty lists to save data of chunks. Dump the data every 5 rows.
    class_id_lt = []
    prompt_token_lt = []
    completion_token_lt = []

    # Create error lists to save classes that cannot be processed. Dump the data every 5 rows.
    class_error = []
    link_error = []

    print(class_id_chunk)

    for index, i in enumerate(class_id_chunk):
        try:
            # Class number
            class_number = i
            
            # Method 1: Extract readings with parsed text breaking it into trunks

            # Words per trunks
            max_words = 800
            
            # Run API
            text_chunks_prompt_token, text_chunks_completion_token = extract_with_text(class_file, i, max_words)

            # Append values to list
            class_id_lt.append(i)
            prompt_token_lt.append(text_chunks_prompt_token)
            completion_token_lt.append(text_chunks_completion_token)

            # Method 2: Extract readings with screenshots
            # image_prompt_token, image_completion_token = extract_with_image(i)

            # Method 3: Extract readings with screenshots and text
            # image_text_prompt_token, image_text_completion_token = extract_with_images_text(i)

            # Method 4: Extract readings with parsed text without breaking it into trunks
            # max_words = 100000000
            # text_prompt_token, text_completion_token = extract_with_text(i, max_words)
        
        except Exception as e:
            # Handle any exception, log error and continue with the next iteration
            print(f"Error processing class {i}: {e}")
            class_error.append(i)
            link_error.append(links_chunk[index])

    print("#### Dumping Data ####")
    # Turn token usage into dataframe
    token_dct = {"Class ID": class_id_lt, "Prompt Token": prompt_token_lt, "Completion Token": completion_token_lt}

    # Turn chunk data into dataframe           
    df_token = pd.DataFrame(token_dct)

    # Judge if the path exists
    if os.path.exists(filename):
        # Appending chunk data to the excel file 
        with pd.ExcelWriter(filename, mode = 'a', if_sheet_exists = 'overlay') as writer:
            # Access the existing sheet
            sheet = writer.sheets['Sheet1']

            # Determine the last row with data
            startrow = sheet.max_row
            
            # Write the DataFrame starting from the next row
            df_token.to_excel(writer, sheet_name='Sheet1', startrow=startrow, index=False, header=False)
    else:
        # Create a excel file
        with pd.ExcelWriter(filename) as writer:  
            df_token.to_excel(writer, sheet_name='Sheet1', index=False)


    # Update the number of rows to skip for the next iteration
    skip_rows += chunk_size

    # Turn error data into dataframe
    error_dct =  {"Class ID": class_error, "Links": link_error}

    # Turn error data into dataframe
    df_error = pd.DataFrame(error_dct)

    # Judge if the path exists
    if os.path.exists(error_file):
        # Appending chunk data to the excel file 
        with pd.ExcelWriter(error_file, mode = 'a', if_sheet_exists = 'overlay') as writer2:  

            # Access the existing sheet
            sheet2 = writer2.sheets['Sheet1']

            # Determine the last row with data
            startrow2 = sheet2.max_row
            
            # Write the DataFrame starting from the next row
            df_error.to_excel(writer2, sheet_name='Sheet1', startrow=startrow2, index=False, header=False)
    else:
        # Create a excel file
        with pd.ExcelWriter(error_file) as writer2:  
            df_error.to_excel(writer2, sheet_name='Sheet1', index=False)
