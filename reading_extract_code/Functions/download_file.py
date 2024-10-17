# The code in this file is to download files from Google and web PDF.

import requests
import gdown
import os

#Download the Google file locally

def google_access(url, class_folder, class_id):
    google_file_id = url.split('/d/')[1].split('/')[0]
    
    if "document" in url:
        #Download the doc as a PDF
        download_url = f"https://docs.google.com/document/d/{google_file_id}/export?format=pdf"
    elif "file" in url:
        download_url = f"https://drive.google.com/uc?id={google_file_id}"
    else:
        output_path = "error"

    # Create the directory if it doesn't exist
    if not os.path.exists(class_folder):
        os.makedirs(class_folder)
    
    output_path = f"{class_folder}/{class_id}/{class_id}_syllabus.pdf"

    # Download the file using gdown
    gdown.download(download_url, output=output_path, quiet=False)
    
    print(f"Download url: {download_url}")
    print(f"File downloaded successfully to: {output_path}")
    
    return output_path


# Download the web PDF and save it locally.

def download_pdf(url, class_folder, class_id):
    response = requests.get(url)
    if response.status_code == 200:
        # Create the directory if it doesn't exist
        if not os.path.exists(class_folder):
            os.makedirs(class_folder)

        # Define the full path to save the PDF
        output_path = f"{class_folder}/{class_id}/{class_id}_syllabus.pdf"
        
        # Save the PDF content to the file
        with open(output_path, 'wb') as f:
            f.write(response.content)
            
        print(f"PDF successfully downloaded and saved to {local_path}")
    else:
        output_path = "error"
        print("PDF fails to be downloaded")
    return output_path