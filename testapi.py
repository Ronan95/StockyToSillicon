from bs4 import BeautifulSoup
import requests
from datetime import datetime
from colorama import Fore, Style, init
from pyfiglet import figlet_format


init()

BASE = "http://localhost:5000/"

STOCKS_INFO = [
    {
        "name": "KO",
        "US": "https://es-us.finanzas.yahoo.com/quote/KO?p=KO", 
        "BA": "https://es-us.finanzas.yahoo.com/quote/KO.BA?p=KO.BA&.tsrc=fin-srch&guccounter=1",
        "multiplier": 5
    },

    {
        "name": "AAPL",
        "US": "https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch", 
        "BA": "https://finance.yahoo.com/quote/AAPL.BA?p=AAPL.BA&.tsrc=fin-srch",
        "multiplier": 10
    },

    {
        "name": "GOLD",
        "US": "https://finance.yahoo.com/quote/GOLD?p=GOLD&.tsrc=fin-srch", 
        "BA": "https://finance.yahoo.com/quote/GOLD.BA?p=GOLD.BA&.tsrc=fin-srch",
        "multiplier":1
    },

    {
        "name": "TSLA",
        "US": "https://finance.yahoo.com/quote/TSLA?p=TSLA&.tsrc=fin-srch", 
        "BA": "https://finance.yahoo.com/quote/TSLA.BA?p=TSLA.BA&.tsrc=fin-srch",
        "multiplier":15
    },

    {
        "name": "AMZN",
        "US": "https://finance.yahoo.com/quote/AMZN?p=AMZN&.tsrc=fin-srch", 
        "BA": "https://finance.yahoo.com/quote/AMZN.BA?p=AMZN.BA&.tsrc=fin-srch",
        "multiplier":144
    },
    {
        "name": "MSFT",
        "US": "https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch", 
        "BA": "https://finance.yahoo.com/quote/MSFT.BA?p=MSFT.BA&.tsrc=fin-srch",
        "multiplier":10
    },
     {
        "name": "NFLX",
        "US": "https://finance.yahoo.com/quote/NFLX?p=NFLX&.tsrc=fin-srch", 
        "BA": "https://finance.yahoo.com/quote/NFLX.BA?p=NFLX.BA&.tsrc=fin-srch",
        "multiplier":16
    },
    {
        "name": "FB",
        "US": "https://finance.yahoo.com/quote/FB?p=FB&.tsrc=fin-srch", 
        "BA": "https://finance.yahoo.com/quote/FB.BA?p=FB.BA&.tsrc=fin-srch",
        "multiplier":8
    },
     {
        "name": "GOOGL",
        "US": "https://finance.yahoo.com/quote/GOOGL?p=GOOGL&.tsrc=fin-srch", 
        "BA": "https://finance.yahoo.com/quote/GOOGL.BA?p=GOOGL.BA&.tsrc=fin-srch",
        "multiplier":58
    },
    {
        "name": "AUY",
        "US": "https://finance.yahoo.com/quote/AUY?p=AUY&.tsrc=fin-srch", 
        "BA": "https://finance.yahoo.com/quote/AUY.BA?p=AUY.BA&.tsrc=fin-srch",
        "multiplier":1
    }

]


def get_date():
    return "[" + str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + "]"



def get_ccl(ba_price, us_price, multiplier=1):
    return ba_price/us_price * multiplier


def get_stock_price(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    stock = soup.find_all(
        "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].text
    

    price = float(stock.replace(",", ""))

    return price



def get_stocks():
    print(f'{Style.BRIGHT}{Fore.YELLOW}{get_date()}{Fore.RESET} Fetching current stock prices...{Style.RESET_ALL}\n')

    stocks = []

    for stock_info in STOCKS_INFO:
        name = stock_info['name']
        us_url = stock_info['US']
        ba_url = stock_info['BA']
        multiplier = stock_info['multiplier']

        us_price = get_stock_price(us_url)
        ba_price = get_stock_price(ba_url)

        ccl = get_ccl(ba_price, us_price, multiplier=multiplier)

        stocks.append({
            'name':name,
            'price':ccl
        })  

    return stocks

print(Style.BRIGHT + Fore.RESET + figlet_format("Stocky Scraper"))


################## CREATE STOCKS ##################

create_stocks = True if input(f'{Style.BRIGHT}{Fore.YELLOW}[*]{Fore.RESET} Create stocks? [y/n]: {Fore.GREEN}') == 'y' else False
print()

if create_stocks:
    stocks = get_stocks()

    for i in range(len(stocks)):
        response = requests.put(BASE + "stock/create", data=stocks[i])
        new_stock = response.json()
        print(f'{Style.BRIGHT}{Fore.YELLOW}[+]{Fore.RESET} New stock created: {Fore.GREEN}{new_stock}{Style.RESET_ALL}')

    print()




################## UPDATE STOCKS ##################

try:
    while True:
        stocks = get_stocks()

        for i in range(len(stocks)):
            stock = stocks[i]
            response = requests.post(BASE + f"stock/{stock['name']}/update", data={'price':stock['price']})
            updated_stock = response.json()
            print(f'{Style.BRIGHT}{Fore.YELLOW}[+]{Fore.RESET} Stock updated: {Fore.GREEN}{updated_stock}{Style.RESET_ALL}')

        print()

        stocks= requests.get('localhost:5000/stock/all')

        stocks= stocks.json()

        for stock in stocks:
            print(f'{stock["name"]}, {stock["price"]}')
        
        print()


except KeyboardInterrupt:
    pass