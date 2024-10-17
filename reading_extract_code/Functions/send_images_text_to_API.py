# The code in this file sends syllabus screenshots to API. 2 screenshots at one time.

import base64
import requests
import os
import pdb
from openai import OpenAI

# Count number of images in a folder
def count_images_in_folder(class_folder, class_id, extensions=[".png"]):
    # Count the number of image files in the folder with the specified extensions
    folder_path = f'{class_folder}/{class_id}'
    image_count = 0
    for file_name in os.listdir(folder_path):
        if any(file_name.lower().endswith(ext) for ext in extensions):
            image_count += 1
    return image_count

# Read API prompt
def read_prompt(syllabus_with_url):
    file = open('/Users/ninachen/Desktop/reading_extract_code/Prompts/Find Reading Prompt text + image.txt','r')
    content = file.read()
    content_with_syllabus = content.replace("{{html}}", syllabus_with_url)
    file.close()
    return content_with_syllabus

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Append messages sent to API
def message_sent_API(image_start, image_end, class_folder, class_id):

    # Original message
    original_message =  [
        {
          "type": "text",
          "text": "What are readings mentioned in this syllabus? Analyze the input screenshots.}"
        }
    ]
    
    for k in range(image_start, image_end):
        
        # Get image path
        image_path = f"{class_folder}/{class_id}/{k}.png"
        print(image_path)

         # Getting the base64 string
        base64_image = encode_image(image_path)
        image_message = {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
        #Append messages
        original_message.append(image_message)
    return original_message


def api_process_images(original_message, prompt_content, syllabus_with_url):

    print("processing----------------")
    results = []
    client = OpenAI(api_key = "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")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages =  [
            {"role": "system", "content": prompt_content},
            {"role": "user", "content": original_message}]
    )
    results = response.choices[0].message.content
    token_used  = response.usage.total_tokens
    return results, token_used

# Send screenshots and parsed syllabus to API everytime
def send_images_text(class_folder, class_id, batch_size, syllabus_with_url):

    total_tokens = 0

    # Count number of images
    image_count = count_images_in_folder(class_folder, class_id)
    print(f"There are {image_count} images in the folder.")

    # Loading API content
    prompt_content = read_prompt(syllabus_with_url)

    full_result = []
    image_id_total = image_count - 1

    print(f'Total image count is {image_count}. Send images into API in batch size {batch_size}')

    # Send images to API in batches
    for i in range(0, image_count, batch_size):
        image_start = i
        image_end = i + batch_size
            
        if image_end > image_id_total:
            image_end = image_count

        print(f"image_start + {image_start}")
        print(f"image_end + {image_end}")
            
        # Generate messages for the screenshots
        original_message = message_sent_API(image_start, image_end, class_folder, class_id)

        # Get results for the screenshots
        results, tokens_single = api_process_images(original_message, prompt_content, syllabus_with_url)

        # Append result to full results
        full_result.append(results)

        # Count total tokens used
        total_tokens += tokens_single
        print(f"Current image input uses {tokens_single} tokens")
    
    print(f"Initial API image extraction uses {total_tokens} tokens")
    return full_result, total_tokens