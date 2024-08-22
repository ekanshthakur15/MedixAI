import json
import time

import google.generativeai as genai

# function to upload files to Gemini.

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Function to wait for files to open

def wait_for_files_active(files):
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

# Function to convert json string into JSON object
def create_json(json_string):

    cleaned_string = json_string.strip("```json")
    print("Cleaned_1: " + cleaned_string)
    n = len(cleaned_string)
    cleaned_string = cleaned_string[:n-4]
    print("Cleaned_1: " + cleaned_string)


    try:
        json_object = json.loads(cleaned_string)
        return json_object
    except json.JSONDecodeError as e:
        return e