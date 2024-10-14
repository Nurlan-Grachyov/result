from datetime import datetime

import pandas as pd

from src.services import path_to_project

path_to_file = path_to_project / "data" / "operations.xlsx"
df_file = pd.read_excel(path_to_file)

date_obj = datetime(2021, 5, 6)
str_date = datetime.strftime(date_obj, "%Y-%m")

def spending_by_weekday(file, date='14.10.2024'):
    transactions = []
    for index, row in file.iterrows():
        row_data = row.to_dict()
        transactions.append({"Дата платежа": row_data["Дата платежа"],
                            "Сумма платежа": row_data["Сумма платежа"]})



spending_by_weekday(df_file, str_date)
