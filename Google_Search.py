import requests
from bs4 import BeautifulSoup
import time
from termcolor import colored
import smtplib
from email.mime.text import MIMEText
def answer_question(question, answers):
        start_time = time.time()

        Question = f"{question}"
        a = "{}".format(Question + f" {answers[0]}")
        b = "{}".format(Question + f" {answers[1]}")
        c = "{}".format(Question + f" {answers[2]}")
        #print(Question)

        # Amount Of Search Results
        # A
        r = requests.get("https://www.google.com/search", params={'q':a})
        soup = BeautifulSoup(r.text, "lxml")
        res = soup.find("div", {"id": "resultStats"})

        # B
        r = requests.get("https://www.google.com/search", params={'q':b})
        soup = BeautifulSoup(r.text, "lxml")
        res1 = soup.find("div", {"id": "resultStats"})

        # C
        r = requests.get("https://www.google.com/search", params={'q':c})
        soup = BeautifulSoup(r.text, "lxml")
        res2 = soup.find("div", {"id": "resultStats"})

        # Removes words; leaves just numbers

        integers = []
        for i in res.text:
            if i.isdigit():
                integers.append(i)
        ''.join(integers)

        integers1 = []
        for i in res1.text:
            if i.isdigit():
                integers1.append(i)
        ''.join(integers1)

        integers2 = []
        for i in res2.text:
            if i.isdigit():
                integers2.append(i)
        ''.join(integers2)


        fullmax = []
        fullmax.append(''.join(integers))
        fullmax.append(''.join(integers1))
        fullmax.append(''.join(integers2))

        max_value = max([int(i) for i in fullmax])


        if int(max_value) == int(fullmax[0]):
            print(colored(f'{answers[0]}\n', 'green'))
            CR = f"{answers[0]}"
        if int(max_value) == int(fullmax[1]):
            print(colored(f'{answers[1]}\n', 'green'))
            CR = f"{answers[1]}"
        if int(max_value) == int(fullmax[2]):
            print(colored(f'{answers[2]}\n', 'green'))
            CR = f"{answers[2]}"

        a = "CURRENT  RUNTIME : %s seconds " % str(round(time.time() - start_time, 2))

        print(colored(a, "green"))



