import os
import openai
import datetime
import getpass
import time
from termcolor import colored

try:
    with open("openai_api_key.txt", "r") as file:
        api_key = file.read().strip()
        openai.api_key = api_key
except:
    print(colored("파일이 없음.", "red"))
    print(colored("키를 생성해야 합니다.", "yellow"))
    api_key = getpass.getpass("OpenAI API key: ")
    openai.api_key = api_key
    with open("openai_api_key.txt", "w") as file:
        file.write(api_key)

model_engine = "gpt-3.5-turbo-0125"

if not os.path.exists("logs"):
    os.makedirs("logs")

messages = []


def send_message(message, chatbot_name):
    if not messages:
        messages.append({"role": "system", "content": chatbot_name})
    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages
    )

    return response["choices"][0]["message"]["content"]


def save_history(history, filename):
    with open(filename, "a", encoding="UTF8") as file:
        file.write(history + "\n")


def main():
    current_time = datetime.datetime.now().strftime("%d.%m.%Y_%H_%M")

    default_chatbot_name = "챗봇"
    chatbot_name = input(colored("챗봇의 이름을 정해주세요(기본은 챗봇입니다) ", "yellow")) or default_chatbot_name

    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    filename = f"{logs_dir}/{chatbot_name.replace(' ', '_')}_{current_time}.txt"

    while True:
        message = input(colored("사용자: ", "cyan"))

        if message == "종료":
            break

        response = send_message(message, chatbot_name)

        output_message = colored(f"{chatbot_name}: ", "green") + response
        print(output_message)

        history = f"You: {message}\n{chatbot_name}: {response}\n"
        save_history(history, filename)

        messages.append({"role": "user", "content": message})
        messages.append({"role": "assistant", "content": response})

        time.sleep(1)


main()
