# The code in this file sends readings from first API along with extracted text with url abbreviations to API.
from openai import OpenAI
import pdb

def text_reading_sent_message(df, syllabus_with_url):

    # If the dataframe is empty, directly end the function.
    if df.empty:
        results_with_url = None
        text_prompt_token_used = 0
        text_completion_token_used = 0
        return results_with_url, text_prompt_token_used, text_completion_token_used

    # Read add url abbreviation for each reading name
    reading_df = df['Reading Name']

    # Extract only the 'Reading Name' column
    reading_name = reading_df.tolist()

    # Retrieve the prompt to find url abbreviation for each reading name
    def read_URL_prompt():
        file = open('/Users/ninachen/Desktop/privacy_syllabus/reading_extract_code/Prompts/Find URL Prompt.txt','r')
        content_URL_Prompt = file.read()
        file.close()
        return content_URL_Prompt
    
    # Get url inserted into excel
    get_url_prompt = read_URL_prompt()

    client = OpenAI(api_key = "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")

    print("-------API starts identifying readings in the parsed text ---------")

    response2 = client.chat.completions.create(
    model="gpt-4o",
    messages =  [
        {"role": "system", "content": get_url_prompt},
        {"role": "user", "content": f"Here is the parsed text with url abbreviations: {syllabus_with_url}; Here is the dataframe of reading names: {reading_name}"}],
    temperature = 0
    )

    # Count number of tokens used
    token_used  = response2.usage.total_tokens

    results_with_url = response2.choices[0].message.content

    # Calculate tokens used
    text_prompt_token_used = response2.usage.prompt_tokens
    text_completion_token_used = response2.usage.completion_tokens

    return results_with_url, text_prompt_token_used, text_completion_token_used

