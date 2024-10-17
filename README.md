# privacy_syllabus

## reading_extract_code
This folder is for extracting readings from syllabi, including reading name, author name, published year and url.
It contains three different input methods: image only, image with text and text.
- `extract_with_image.py`: send screenshots into API.
- `extract_with_images_and_text.py`: send screenshots and parsed syllabus text to API.
- `extract_with_text_in_chunks.py`: send (chunnked) text to API.

## first_classifier
This folder is for using API to classify reading content into: definition, risk, protection and other.
- `extract_privacy_content_V2.py`: extract sentences containing keyword "privacy". 
- `api_classification.ipynb`: classify readings using API.
