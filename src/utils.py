import json
import os
from datetime import datetime
from pathlib import Path

import openpyxl
import requests
from dotenv import load_dotenv


def read_file():
    path_to_project = Path(__file__).resolve().parent.parent
    path_to_file = path_to_project / "data" / "operations.xlsx"

    workbook = openpyxl.load_workbook(path_to_file)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]

    transactions = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))
        transactions.append(
            {
                "Дата операции": row_data["Дата операции"],
                "Дата платежа": row_data["Дата платежа"],
                "Номер карты": row_data["Номер карты"],
                "Статус": row_data["Статус"],
                "Сумма операции": row_data["Сумма операции"],
                "Валюта операции": row_data["Валюта операции"],
                "Сумма платежа": row_data["Сумма платежа"],
                "Валюта платежа": row_data["Валюта платежа"],
                "Кэшбэк": row_data["Кэшбэк"],
                "Категория": row_data["Категория"],
                "MCC": row_data["MCC"],
                "Описание": row_data["Описание"],
                "Бонусы (включая кэшбэк)": row_data["Бонусы (включая кэшбэк)"],
                "Округление на инвесткопилку": row_data["Округление на инвесткопилку"],
                "Сумма операции с округлением": row_data["Сумма операции с округлением"],
            }
        )
        if len(transactions) == 100:
            break
        return transactions

read_file = read_file()
# print(read_file)


def greeting():
    date = datetime.now()
    str_date = date.strftime("%Y-%m-%d %H:%M:%S")

    hour = str_date[11:13]
    info = {}
    if 4 <= int(hour) < 12:
        info["greeting"] = "Доброе утро"
        return info
    elif 12 <= int(hour) < 18:
        info["greeting"] = "Добрый день"
        return info
    elif 18 <= int(hour) < 22:
        info["greeting"] = "Добрый вечер"
        return info
    else:
        info["greeting"] = "Доброй ночи"
        return info

greeting = greeting()
# print(greeting)

def cards(trans, info):
    info["cards"] = []
    for transaction in trans:
        if transaction.get("Номер карты") is not None:
            last_digits = transaction.get("Номер карты")[1:]
            if not any(card["last_digits"] == last_digits for card in info["cards"]):
                info["cards"].append({"last_digits": last_digits, "total_spent": 0, "cashback": 0})
            for card in info["cards"]:
                if card["last_digits"] == last_digits:
                    if "-" in str(transaction["Сумма платежа"]):
                        amount = str(transaction["Сумма платежа"])[1:]
                        cash_back = float(amount) / 100
                    else:
                        continue
                    card["total_spent"] += float(amount)
                    card["cashback"] += cash_back
    return info


cards(read_file, greeting)
cards = cards(read_file, greeting)
# print(cards)

def top_transactions(trans, info):
    top = sorted(trans, key=lambda x: x["Сумма операции"])[:5]
    info["top_transactions"] = []
    for trans in top:
        info["top_transactions"].append(
            {
                "date": trans["Дата платежа"],
                "amount": trans["Сумма операции"],
                "category": trans["Категория"],
                "description": trans["Описание"],
            }
        )
    return info


top_transactions(read_file, cards)
top_transactions = top_transactions(read_file, cards)
# print(top_transactions)

def currency(info):
    # load_dotenv()
    # access_key = os.getenv("access_key")
    #
    # headers_curr = {"apikey": access_key}
    # url_usd = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD"
    #
    # result_usd = requests.get(url_usd, headers=headers_curr)
    # new_amount_usd = result_usd.json()
    #
    # url_eur = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=EUR"
    # result_eur = requests.get(url_eur, headers=headers_curr)
    # new_amount_eur = result_eur.json()

    info["currency_rates"] = []

    #     info['currency_rates'].append({
    #   "currency": "USD",
    #   "rate": new_amount_usd['rates']['RUB']
    # })
    #
    #     info['currency_rates'].append({
    #         "currency": "EUR",
    #         "rate": new_amount_eur['rates']['RUB']
    #     })

    info["currency_rates"].append({"currency": "USD", "rate": 95.676332})

    info["currency_rates"].append({"currency": "EUR", "rate": 104.753149})
    return info


currency(top_transactions)
currency = currency(top_transactions)
# print(currency)


def stock_prices(trans, info):
    import http.client

    conn = http.client.HTTPSConnection("real-time-finance-data.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "39ac2ff51amshbf14c0ab2c03d5cp1bb809jsnc4631bcad964",
        'x-rapidapi-host': "real-time-finance-data.p.rapidapi.com"
    }

    conn.request("GET", "/market-trends?trend_type=MARKET_INDEXES&country=us&language=en", headers=headers)

    res = conn.getresponse()
    data = res.read()
    data_json = json.loads(data.decode("utf-8"))

    info["stock_prices"] = []

    for trend in data_json['data']['trends']:

        info["stock_prices"].append(
            {
                "stock": trend['name'],
                "price": trend['price']
            }
        )

    print(info)

stock_prices(read_file, currency)