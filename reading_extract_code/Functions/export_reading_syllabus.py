# Export reading as a spreadsheet and add class ID.

import json
import pandas as pd

def export_reading_syllabus(results, class_id, class_folder, url_mappings, chunk_number):

    total_df = pd.DataFrame(columns=['Reading Name', 'Author Name', 'Published Year', 'Page Numbers to Read', 'URL'])
    
    for i in range(chunk_number):
        reading = json.loads(results[i].replace("```json","").replace("```","").replace("\n",""))
        df = pd.DataFrame(reading)
        total_df = pd.concat([total_df, df], ignore_index=True) 

    # #Count the number of rows in the DataFrame
    # num_rows = len(total_df)
    
    # #Add class_id in the new column
    # total_df['Class ID'] = [f"{class_id}"] * num_rows

    # Replace URL abbreviations with actual URLs from the url_mappings dictionary, handling multiple URLs
    total_df['URL'] = total_df['URL'].apply(lambda x: ', '.join([url_mappings.get(url.strip(), url.strip()) for url in x.split(',')]))


        
    # Save to an Excel spreadsheet
    output_file = f"{class_folder}/{class_id}/{class_id}_readings.xlsx"
    total_df.to_excel(output_file, index=False)