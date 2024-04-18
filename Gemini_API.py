import google.generativeai as gemini
import os
import datetime
import getpass
import time
from termcolor import colored


def init_gemini():
    try:
        with open("google_api_key.txt", "r") as file:
            api_key = file.read().strip()
            gemini.configure(api_key=api_key)

    except:
        print(colored("파일이 없음.", "red"))
        print(colored("키를 생성해야 합니다.", "yellow"))
        api_key = getpass.getpass("GOOGLE API key: ")
        gemini.configure(api_key=api_key)
        with open("google_api_key.txt", "w") as file:
            file.write(api_key)

    generation_config = {
        "temperature": 0.5,
        "top_p": 0.1,
        "top_k": 1,
        "max_output_tokens": 2048
    }

    model = gemini.GenerativeModel(model_name="gemini-pro",
                                   generation_config=generation_config)

    return model

def send_message(model, message):
    conv = model.start_chat(history=[
        {"role": "user", "parts": [prompts_text]},
        {"role": model, "parts": ["what would you like me to rewriter?"]}
    ])
    conv.send_message(message)

    response_text = ''.join(part.get('text', '') for part in conv.last.parts)
    return response_text

model = init_gemini()

message = input()

response = send_message(model, message)
print(response)