import os
from datetime import datetime
from pathlib import Path
import openpyxl

import requests
from dotenv import load_dotenv

date = datetime.now()
str_date = date.strftime('%Y-%m-%d %H:%M:%S')

def main(func_date):
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
    # print(transactions)
    def greeting():
        hour = func_date[11:13]
        info = {}
        if 4 <= int(hour) < 12:
            info['greeting'] = 'Доброе утро'
            return info
        elif 12 <= int(hour) < 18:
            info['greeting'] = 'Добрый день'
            return info
        elif 18 <= int(hour) < 22:
            info['greeting'] = 'Добрый вечер'
            return info
        else:
            info['greeting'] = 'Доброй ночи'
            return info
    # print(greeting())

    def cards(trans, info):
        info['cards'] = []
        total_spent = {}
        print(info)
        for transaction in trans:
            if transaction.get('Номер карты') is not None:
                last_digits = transaction.get('Номер карты')[1:]
                if not any(card["last_digits"] == last_digits for card in info['cards']):
                    info['cards'].append({"last_digits": last_digits, "total_spent" : 0, "cashback" : 0})
                for card in info['cards']:
                    if card['last_digits'] == last_digits:
                        if '-' in str(transaction['Сумма платежа']):
                            amount = str(transaction['Сумма платежа'])[1:]
                            cash_back = float(amount) / 100
                        else:
                            continue
                        card['total_spent']  += float(amount)
                        card['cashback'] += cash_back
        return info

    cards(transactions, greeting())
    cards = cards(transactions, greeting())
    # print(cards)


    def top_transactions(trans, info):
        top = sorted(trans, key=lambda x: x['Сумма операции'])[:5]
        info["top_transactions"] = []
        for trans in top:
            info["top_transactions"].append({
      "date": trans['Дата платежа'],
      "amount": trans['Сумма операции'],
      "category": trans["Категория"],
      "description": trans["Описание"]
    })
        return info
    top_transactions(transactions, cards)
    top_transactions = top_transactions(transactions, cards)
    # print(top_transactions)

    def currency(trans, info):

        load_dotenv()
        access_key = os.getenv("access_key")

        headers_curr = {"apikey": access_key}
        url_usd = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD"

        result_usd = requests.get(url_usd, headers=headers_curr)
        new_amount_usd = result_usd.json()
        print(new_amount_usd)

        url_eur = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=EUR"
        result_eur = requests.get(url_eur, headers=headers_curr)
        new_amount_eur = result_eur.json()
        print(new_amount_eur)

    currency(transactions, top_transactions)

main(str_date)