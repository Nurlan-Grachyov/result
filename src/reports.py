import json
from datetime import datetime

import pandas as pd
from black.trans import defaultdict
from dateutil.relativedelta import relativedelta

from src.services import path_to_project

path_to_file = path_to_project / "data" / "operations.xlsx"
df_file = pd.read_excel(path_to_file)
path_to_json = path_to_project / "data" / "spending_by_weekday.json"
path_to_json_2 = path_to_project / "data" / "spending_by_weekday_2.json"


date_obj = datetime(2021, 5, 6)
str_date = datetime.strftime(date_obj, "%d.%m.%Y")
def my_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open(path_to_json, "w", encoding="utf-8") as file:
            json.dump(result, file)
        return result

    return wrapper


def decorator_with_args(file):
    def my_big_decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(file, "w", encoding="utf-8") as file_2:
                json.dump(result, file_2)
            return result

        return wrapper

    return my_big_decorator


@decorator_with_args(path_to_json_2)
def spending_by_weekday(file, date="14.10.2022"):
    transactions = []
    to_date = datetime.strptime(date, "%d.%m.%Y")
    from_date = to_date - relativedelta(months=3)

    for index, row in file.iterrows():
        date_payment = row["Дата платежа"]
        amount = row["Сумма платежа"]
        if isinstance(date_payment, str) and isinstance(amount, (float, int)) and amount < 0:
            date_payment = datetime.strptime(date_payment, "%d.%m.%Y")
            if from_date <= date_payment <= to_date:
                weekday = date_payment.strftime("%A")
                transactions.append({weekday: amount})

    spending_per_day = defaultdict(list)
    for trans in transactions:
        for key, value in trans.items():
            spending_per_day[key].append(value)

    spending_per_day = dict(spending_per_day)
    averages = {}
    for key, values in spending_per_day.items():
        avg = sum(values) / len(values)
        averages[key] = round(avg, 2)

    average_json = json.dumps(averages)
    return average_json


if __name__ == "__main__":
    print(spending_by_weekday(df_file, str_date))
