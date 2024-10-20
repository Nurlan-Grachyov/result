from datetime import datetime, timedelta

import pandas as pd

from src.utils import currency, greeting, number_cards, read_file, stock_prices, to_file, top_transactions
from src.utils import path_to_file

begin_date = datetime(2020, 5, 25, 15, 46, 57)
str_begin_date = datetime.strftime(begin_date, "%d-%m-%Y %H:%M:%S")


def get_operations() -> pd.DataFrame:

    df = pd.read_excel(path_to_file)

    datetime_fields_to_convert = {
        "Дата операции": "%d.%m.%Y %H:%M:%S",
        "Дата платежа": "%d.%m.%Y",
    }
    for datetime_field, str_format in datetime_fields_to_convert.items():
        df[datetime_field] = pd.to_datetime(df[datetime_field], format=str_format)

    return df


def filter_operations_by_date(df: pd.DataFrame, date: str):
    dt = datetime.strptime(date, "%d-%m-%Y %H:%M:%S")
    start_date = pd.to_datetime(dt.replace(day=1))
    end_date = pd.to_datetime(dt + timedelta(days=1))
    return df.loc[(df["Дата операции"] >= start_date) & (df["Дата операции"] < end_date)]


def main(analysis_date):
    df = get_operations()
    df = filter_operations_by_date(df, analysis_date)
    return df


main(str_begin_date)

# if __name__ == "__main__":
# print(read_file(main(str_begin_date)))
# greeting()
# print(number_cards(read_file(main(str_begin_date)), greeting()))
# top_transactions(read_file(df), number_cards(read_file(df),greeting()))
# currency(top_transactions(read_file(df), number_cards(read_file(df),greeting())))
# stock_prices(currency(top_transactions(read_file(df), number_cards(read_file(df),greeting()))))
# print(to_file(stock_prices(currency(top_transactions(number_cards(read_file(df), greeting()))))))
# print(
#     to_file(
#         stock_prices(
#             currency(
#                 top_transactions(
#                     read_file(main(str_begin_date)), number_cards(read_file(main(str_begin_date)), greeting())
#                 )
#             )
#         )
#     )
# )
# print(to_file(stock_prices(currency(top_transactions(read_file(df), number_cards(read_file(df), greeting()))))))
# print(currency(
#                 top_transactions(
#                     read_file(main(str_begin_date)), number_cards(read_file(main(str_begin_date)), greeting())
#                 )
#             )
#         )
