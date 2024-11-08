# The code in this file get content with url abbreviations and url mappings from web and downloaded PDF.


# Get content from the syllabus website and replace url with abbreviation
import requests
import re
import pdb
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def complete_url(path, base):
    if not path.startswith(('http', 'https')):
        # Combine the domain and path if it starts with "/"
        return urljoin(base, path)
    else:
        # Return the path as is if it doesn't start with "/"
        return path

def parse_website_with_mappings(url):
    print(url)
    url_mapping = {}
    reason = ""

    try:
        response = requests.get(url)
        
        # Parse the webpage with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
    
        # Counter for URL abbreviation
        url_counter = 1
        
        # Iterate over all anchor tags with href attributes
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            href_updated = complete_url(href, url)
            
            # Create a unique abbreviation for the URL (e.g., url_1, url_2)
            abbreviation = f"url_{url_counter}"
            url_mapping[abbreviation] = href_updated
    
            # Modify the link text to include the abbreviation in parentheses
            link.string = f"{link.get_text()} ({abbreviation})"
    
            # Increment the URL counter for the next abbreviation
            url_counter += 1
    
        # Convert the modified soup object back to a string (HTML with modifications)
        
        modified_content = soup.get_text()

        cleaned_content = re.sub(r'\n+', '\n', modified_content)

        
        return cleaned_content, url_mapping, reason

    except requests.exceptions.SSLError:
        modified_content = "error"
        reason = "SSL error"
    
    except requests.exceptions.HTTPError:
        modified_content = "error"
        reason = "HTTP error"


    except requests.exceptions.RequestException:
        modified_content = "error"
        reason = "Request error"
        
    except Exception:
        modified_content = "error"
        reason = "Parsing error - need further investigation"
        
    return modified_content, url_mapping, reason

# Extract PDF content from downloaded syllabus and PDF

import pdfplumber

def extract_text_from_pdf_with_spaces(pdf_file_path):
    url_mapping = {}
    full_text = ""
    url_counter = 1

    # Open the PDF file using pdfplumber
    with pdfplumber.open(pdf_file_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

            # Extract annotations (like hyperlinks) from the page
            if page.annots:
                for annot in page.annots:
                    if annot.get("uri"):
                        url = annot["uri"]
                        abbreviation = f"url_{url_counter}"
                        url_mapping[abbreviation] = url
                        full_text += f" [{abbreviation}]"
                        url_counter += 1

    # Display the updated content and the URL mapping
    return full_text, url_mapping