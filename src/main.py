from src.reports import spending_by_weekday, df_file
from src.services import investment_bank, str_date, transactions
from src.utils import to_file, stock_prices, currency, top_transactions, read_file, number_cards, greeting
from src.views import main, str_begin_date

# print(
#         to_file(
#             stock_prices(
#                 currency(
#                     top_transactions(
#                         read_file(main(str_begin_date)), number_cards(read_file(main(str_begin_date)), greeting())
#                     )
#                 )
#             )
#         )
#     )
#
# print(investment_bank(str_date, transactions, 50))
print(str_date)
# print(spending_by_weekday(df_file, str_date))
