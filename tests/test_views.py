import unittest
from unittest.mock import patch

import pandas as pd

from src.views import get_operations, filter_operations_by_date, main


@patch("src.views.pd.read_excel")
def test_get_operations(mock_excel):
    data = [
        {
            "Дата операции": "26.05.2020 13:29:09",
            "Дата платежа": "28.05.2020",
            "Номер карты": "*7197",
            "Сумма операции": -45.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -45.0,
            "Валюта платежа": "RUB",
        },
        {
            "Дата операции": "26.05.2020 13:23:32",
            "Дата платежа": "28.05.2020",
            "Номер карты": "*7197",
            "Сумма операции": -86.6,
            "Валюта операции": "RUB",
            "Сумма платежа": -86.6,
            "Валюта платежа": "RUB",
        },
    ]

    mock_excel.return_value = pd.DataFrame(data)
    result = get_operations()

    pd.testing.assert_frame_equal(result,mock_excel.return_value)



# def setup():
#         data = [{
#             "Дата операции": "26.05.2020 13:29:09",
#             "Дата платежа": "28.05.2020"},
#             {
#             "Дата операции": "26.05.2020 13:23:32",
#             "Дата платежа": "28.05.2020"
#             }]
#         df = pd.DataFrame(data)
#         return df

# def test_filter_operations_by_valid_date():
#         date = "26-05-2026 00:00:00"
#         filtered_df = filter_operations_by_date(setup(), date)
#
#         expected_data = [{
#             "Дата операции": "26.05.2020 13:29:09",
#             "Дата платежа": "28.05.2020"},
#             {
#             "Дата операции": "26.05.2020 13:23:32",
#             "Дата платежа": "28.05.2020"
#             }]
#         expected_df = pd.DataFrame(expected_data)
#
#         pd.testing.assert_frame_equal(filtered_df, expected_df)
#
#
# def test_main(return_time_for_main):
#     data = 'test'
#     excel_data = pd.DataFrame(data)
#     mock_read_excel.return_value = pd.DataFrame(data)
#     assert main(return_time_for_main) == excel_data


@patch.object(pd, 'read_excel')
def test_filter_operations_by_date(mock_read_excel):
    date = "26-05-2026 00:00:00"
    data = [{
            "Дата операции": "26.05.2020 13:29:09",
            "Дата платежа": "28.05.2020"},
            {
            "Дата операции": "26.05.2020 13:23:32",
            "Дата платежа": "28.05.2020"
            }]
    mock_read_excel.return_value = pd.DataFrame(data)
    assert filter_operations_by_date(mock_read_excel.return_value, date) == [{
            "Дата операции": "26.05.2020 13:29:09",
            "Дата платежа": "28.05.2020"},
            {
            "Дата операции": "26.05.2020 13:23:32",
            "Дата платежа": "28.05.2020"
            }]






















