import webbrowser
from termcolor import colored
import datetime
import logging
import os
from . import Google_Search
import time
from datetime import datetime
from lomond import WebSocket
from unidecode import unidecode
import colorama
import requests
import json
import re

def show_not_on():
    colorama.init()
    # Set up logging
    logging.basicConfig(filename="data.log", level=logging.INFO, filemode="w")

    # Read in bearer token and user ID
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            BEARER_TOKEN = settings[0].split("=")[1]
        except IndexError as e:
            logging.fatal(f"Settings read error: {settings}")
            raise e

    print("getting")
    main_url = f"https://api-quiz.hype.space/shows/now?type="
    headers = {"Authorization": f"Bearer {NzEwODAyMDcxMjI5ODI1MDY1.XsNtkg.F0rN8VnlhpMziT2PUhBk78Hl2q4}:,
               "x-hq-client": "Android/1.3.0"}
    # "x-hq-stk": "MQ==",
    # "Connection": "Keep-Alive",
    # "User-Agent": "okhttp/3.8.0"}

    try:
        response_data = requests.get(main_url).json()
    except:
        print("Server response not JSON, retrying...")
        time.sleep(1)

    logging.info(response_data)

    if "broadcast" not in response_data or response_data["broadcast"] is None:
        if "error" in response_data and response_data["error"] == "Auth not valid":
            raise RuntimeError("Connection settings invalid")
        else:
            print("Show not on.")
            next_time = datetime.strptime(response_data["nextShowTime"], "%Y-%m-%dT%H:%M:%S.000Z")
            now = time.time()
            offset = datetime.fromtimestamp(now) - datetime.utcfromtimestamp(now)

            NextShowTime = f"{(next_time + offset).strftime('%m-%d-%Y %I:%M %p')}"
            NextShowPrize = f"Prize: " + response_data["nextShowPrize"]
            time.sleep(5)
            print(NextShowTime)
            print(NextShowPrize)



def show_active():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()
    return response_data['active']


def get_socket_url():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()

    socket_url = response_data['broadcast']['socketUrl'].replace('https', 'wss')
    return socket_url


def connect_websocket(socket_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}",
               "x-hq-client": "iPhone8,2"}


    websocket = WebSocket(socket_url)

    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))

    for msg in websocket.connect(ping_rate=5):
        if msg.name == "text":
            message = msg.text
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
            message_data = json.loads(message)

            if message_data['type'] == 'question':
                question = message_data['question']
                qcnt = message_data['questionNumber']
                Fullcnt = message_data['questionCount']

                print(f"\nQuestion number {qcnt} out of {Fullcnt}\n{question}")
                #open_browser(question)
                answers = [unidecode(ans["text"]) for ans in message_data["answers"]]
                print(f"\n{answers[0]}\n{answers[1]}\n{answers[2]}\n")
                Google_Search.answer_question(question, answers)

            elif message_data["type"] == "questionSummary":

                answer_counts = {}
                correct = ""
                for answer in message_data["answerCounts"]:
                    ans_str = unidecode(answer["answer"])

                    if answer["correct"]:
                        correct = ans_str
                advancing = message_data['advancingPlayersCount']
                eliminated = message_data['eliminatedPlayersCount']

                print(colored(correct, "blue"))
                print(advancing)
                print(eliminated)



def open_browser(question):

    main_url = "https://www.google.co.in/search?q=" + question
    webbrowser.open_new(main_url)


def get_auth_token():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            auth_token = settings[0].split("=")[1]
        except IndexError:
            print('No Key is given!')
            return 'NONE'

        return auth_token

if __name__ == '__main__':
    input('Press enter to start ')
    if show_active():
        url = get_socket_url()
        print('Connecting to Socket : {}'.format(url))

        token = get_auth_token()
        if token == 'NONE':
            print('Please enter a valid auth token.')
        else:
            connect_websocket(url, token)

    else:
        show_not_on()
