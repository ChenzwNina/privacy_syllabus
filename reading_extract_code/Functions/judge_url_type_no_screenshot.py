# The code in this file judges the type of url (Google PDF, doc, web PDF, web) and perform relative functions.

import pdb
from Functions.download_file import google_access, download_pdf
from Functions.get_content_with_url import extract_text_from_pdf_with_spaces, parse_website_with_mappings

def get_content_and_url(url, class_folder, class_id):
    url_mappings = {}
    reason = ""
    print(url)
    
    if "google" in url.lower() or ".pdf" in url.lower():
        if "google" in url.lower():
            # Download the Google file to local folder as PDF and get its path
            output_path = google_access(url, class_folder, class_id)

            if output_path == "error":
                syllabus_content = "error"
                reason = "Google downloading error"
        else:
            #Download the PDF to local folder and get its path
            print("Download web PDF")
            output_path = download_pdf(url, class_folder, class_id)

            if output_path == "error":
                syllabus_content = "error"
                reason = "PDF downloading error"

        # Get content from downloaded Google files or PDF
        if output_path != "error":
            # Get PDF content
            syllabus_content, url_mappings = extract_text_from_pdf_with_spaces(output_path)
            
    # If it is a website
    else: 
        syllabus_content, url_mappings, reason = parse_website_with_mappings(url)
        
    return syllabus_content, url_mappings, reason

