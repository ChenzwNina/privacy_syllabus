# The code in this file sends text to API.

from openai import OpenAI
client = OpenAI(api_key= "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") #API key here

# Load system_prompt from local files
def load_system_prompt():
    file_path = "/Users/ninachen/Desktop/reading_extract_code/Prompts/Find Reading Prompt text.txt"

    # Open the file in read mode and load the content into a variable
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def split_text_by_words(text, max_words):
    words = text.split()  # Split the text into words
    # If the number of words is less than or equal to max_words, return the text as one chunk
    if len(words) <= max_words:
        return [text]  # No need to split, return the text in a list with one item
    
    # Otherwise, create chunks of up to max_words
    chunks = [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    return chunks

# Use API to run reading extraction
def api_syllabus_classification(syllabus_content, max_words):

    chunks = split_text_by_words(syllabus_content, max_words)

    chunk_number = len(chunks)
    
    results= []

    token_used = 0

    for chunk in chunks:
    #Run GPT-4 for the first round
        response = client.chat.completions.create(
            model= "gpt-4o",
            messages=[
                {"role": "system", "content": load_system_prompt()},
                {"role": "user", "content": f"Identify all readings mentioned in the syllabus:{chunk}"}
            ],
            temperature = 0
            )
        results.append(response.choices[0].message.content)
        sig_tokens = response.usage.total_tokens
        token_used += sig_tokens

    return results, chunk_number, token_used