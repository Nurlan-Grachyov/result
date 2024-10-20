import json

import pandas as pd

from src.reports import spending_by_weekday
from src.services import path_to_project


def test_spending_by_weekday():
    path_to_file = path_to_project / "data" / "operations.xlsx"
    df_file = pd.read_excel(path_to_file)
    data = {'Wednesday': -753.68, 'Tuesday': -549.29, 'Monday': -1356.3, 'Sunday': -1303.8, 'Saturday': -311.52, 'Friday': -2358.73, 'Thursday': -435.24}
    data = json.dumps(data)
    assert spending_by_weekday(df_file, date="14.10.2020") == data
