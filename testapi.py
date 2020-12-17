from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

BASE = "http://localhost:5000/"

#while True:

#KO.US

url_ko_us = "https://es-us.finanzas.yahoo.com/quote/KO?p=KO"
page_ko_us = requests.get(url_ko_us)
soup_ko_us = BeautifulSoup(page_ko_us.text, "html.parser")

ko_us = soup_ko_us.find_all(
    "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].text

#KO.BA

url_ko_ba = "https://es-us.finanzas.yahoo.com/quote/KO.BA?p=KO.BA&.tsrc=fin-srch&guccounter=1"
page_ko_ba = requests.get(url_ko_ba)
soup_ko_ba = BeautifulSoup(page_ko_ba.text, "html.parser")

ko_ba = soup_ko_ba.find_all(
    "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].text

ccl1 = float(ko_ba.replace(",", "")) / float(ko_us.replace(",", "")) * 5

#AAPL.US

url_aapl_us = "https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch"
page_aapl_us = requests.get(url_aapl_us)
soup_aapl_us = BeautifulSoup(page_aapl_us.text, "html.parser")

aapl_us = soup_aapl_us.find_all(
    "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].text

#AAPL.BA

url_aapl_ba = "https://finance.yahoo.com/quote/AAPL.BA?p=AAPL.BA&.tsrc=fin-srch"
page_aapl_ba = requests.get(url_aapl_ba)
soup_aapl_ba = BeautifulSoup(page_aapl_ba.text, "html.parser")

aapl_ba = soup_aapl_ba.find_all(
    "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].text

ccl2 = float(aapl_ba.replace(",", "")) / \
    float(aapl_us.replace(",", "")) * 10

#GOLD.US

url_gold_us = "https://finance.yahoo.com/quote/GOLD?p=GOLD&.tsrc=fin-srch"
page_gold_us = requests.get(url_gold_us)
soup_gold_us = BeautifulSoup(page_gold_us.text, "html.parser")

gold_us = soup_gold_us.find_all(
    "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].text

#GOLD.BA

url_gold_ba = "https://finance.yahoo.com/quote/GOLD.BA?p=GOLD.BA&.tsrc=fin-srch"
page_gold_ba = requests.get(url_gold_ba)
soup_gold_ba = BeautifulSoup(page_gold_ba.text, "html.parser")

gold_ba = soup_gold_ba.find_all(
    "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].text

ccl3 = float(gold_ba.replace(",", "")) / float(gold_us.replace(",", ""))

#TSLA.US

url_tsla_us = "https://finance.yahoo.com/quote/TSLA?p=TSLA&.tsrc=fin-srch"
page_tsla_us = requests.get(url_tsla_us)
soup_tsla_us = BeautifulSoup(page_tsla_us.text, "html.parser")

tsla_us = soup_tsla_us.find_all(
    "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].text

#TSLA.BA

url_tsla_ba = "https://finance.yahoo.com/quote/TSLA.BA?p=TSLA.BA&.tsrc=fin-srch"
page_tsla_ba = requests.get(url_tsla_ba)
soup_tsla_ba = BeautifulSoup(page_tsla_ba.text, "html.parser")

tsla_ba = soup_tsla_ba.find_all(
    "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].text

ccl4 = float(tsla_ba.replace(",", "")) / \
    float(tsla_us.replace(",", "")) * 15

#AMZN.US

url_amzn_us = "https://finance.yahoo.com/quote/AMZN?p=AMZN&.tsrc=fin-srch"
page_amzn_us = requests.get(url_amzn_us)
soup_amzn_us = BeautifulSoup(page_amzn_us.text, "html.parser")

amzn_us = soup_amzn_us.find_all(
    "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].text

#amzn.BA

url_amzn_ba = "https://finance.yahoo.com/quote/AMZN.BA?p=AMZN.BA&.tsrc=fin-srch"
page_amzn_ba = requests.get(url_amzn_ba)
soup_amzn_ba = BeautifulSoup(page_amzn_ba.text, "html.parser")

amzn_ba = soup_amzn_ba.find_all(
    "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].text

ccl5 = float(amzn_ba.replace(",", "")) / \
    float(amzn_us.replace(",", "")) * 144

#ccl_prom = (ccl1 + ccl2 + ccl3 + ccl4 + ccl5) / 5

stocks = [{"name": "KO", "price": str(ccl1)},
          {"name": "AAPL", "price": str(ccl2)},
          {"name": "GOLD", "price": str(ccl3)},
          {"name": "TSLA", "price": str(ccl4)},
          {"name": "AMZN", "price": str(ccl5)}
          ]

for i in range(len(stocks)):
    response = requests.put(BASE + "stock/create", json.dumps(stocks[i]))
    print(response.text)

#input()
#response = requests.get(BASE + "stock/1")
#print(response.json())
