import fitz
import pandas as pd
import re

def extract_paragraphs_with_keyword(pdf_path, keyword, material_ID):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    sentence_endings = re.compile(r'(?<=[.!?]) +')
    
    # Initialize a list to hold the sentences containing the keyword
    paragraphs_with_keyword = []

    # Initialize a list to hold the page num containing the keyword
    page_num_with_keyword = []

    # Iterate through each page in the PDF
    for page_num in range(pdf_document.page_count):
        # Extract text from the page
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        
        # Split the text into sentences
        paragraphs = sentence_endings.split(text)
        
        # Check each sentence for the keyword
        for sentence_num in range(len(paragraphs)):
            paragraph = paragraphs[sentence_num].strip()
            
            if(sentence_num < 1):
                lower_bound = 0
            else:
                lower_bound = sentence_num - 1
            
            if(sentence_num > len(paragraphs) - 2):
                upper_bound = len(paragraphs)
            else:
                upper_bound = sentence_num + 2

            if keyword.lower() in paragraph.lower():
                paragraphs_with_keyword.append(".".join(paragraphs[lower_bound : upper_bound]))
                page_num_with_keyword.append(page_num + 1)

    
    # Close the PDF file
    pdf_document.close()

    result = {"ID": material_ID, "page_num_with_keyword": page_num_with_keyword, "paragraphs_with_keyword": paragraphs_with_keyword}
    return result 


# Fixes error
def clean_illegal_symbols(text):
    if isinstance(text, str):
        return re.sub(r'[\000-\010]|[\013-\014]|[\016-\037]', 'x', text)
    return text


# Usage example
material_ID = "textbook1"
pdf_path = "/Users/ameyakiwalkar/Desktop/Security_Engineering — Second Edition.pdf"
keyword = "privacy"
result = extract_paragraphs_with_keyword(pdf_path, keyword, material_ID)
privacy_df = pd.DataFrame(result)
#drop duplicates
privacy_df = privacy_df.drop_duplicates(subset='paragraphs_with_keyword')
pattern_export = r'/.+?$'
new_path = re.sub(pattern_export, '', pdf_path)

privacy_df = privacy_df.apply(lambda col: col.map(clean_illegal_symbols))

privacy_df.to_excel("/Users/ninachen/Downloads/extracted.xlsx", index = False)