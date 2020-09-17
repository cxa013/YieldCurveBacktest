import csv
import datetime
import math
import collections


with open("T10Y3M.csv") as yc_file:
    yield_curve_obs = collections.defaultdict(list)
    for d in csv.DictReader(yc_file):
        date_obj = datetime.datetime.strptime(d["DATE"],"%Y-%m-%d")
        try:
            yield_curve_obs[date_obj.strftime("%B %Y")].append(float(d["T10Y3M"]))
        except:
            pass

currently_long = True

benchmark_stock_position = 500
stock_position = 500

cash_position = 0

price_at_change = 117.30

records = list()

with open("SP performance.csv", encoding='utf-8-sig') as s_file:
    monthly_data = csv.DictReader(s_file)

    for m in monthly_data:
        month = int(m["Date"].split('.')[1])
        year = int(m["Date"].split('.')[0])
        indx = float(m["Price"])

        #Handle weird September bug
        if m["Date"].split('.')[1] == "1":
            month = 10

        first_day = datetime.datetime(year=year, month=month, day=1)
        month_year = first_day.strftime("%B %Y")
        if month_year in yield_curve_obs:

            spread_less_than_zero = any(s < 0 for s in yield_curve_obs[month_year]) # Any spread less than zero
            average_spread = sum(yield_curve_obs[month_year])/len(yield_curve_obs[month_year])

            print(f"=={month_year}==")
            print(f"Current Spread: {average_spread}")

            # If current position is long and 10 year - 3 month is less than 0
            if currently_long and (spread_less_than_zero):
                # Cash-up existing stock holdings
                cash_position = stock_position * indx

                print(f"Going short. Gain from previous long {(indx-price_at_change) * stock_position}")

                # Go short the same amount we were long
                price_at_change = indx
                stock_position = -stock_position
                currently_long = False


            # If not currently long and spread is never less than zero in the month
            elif not currently_long and not spread_less_than_zero:
                # Book short gains
                cash_position += (stock_position) * (indx-price_at_change)

                print(f"Going long. Gain from previous short {(indx-price_at_change) * stock_position}")
                price_at_change = indx

                # Go long as much stock as possible
                stock_position = math.floor(cash_position/indx)
                cash_position -= stock_position * indx

                currently_long = True

            # Situation Report

            if currently_long:
                net_worth = cash_position + stock_position * indx
            else:
                net_worth = cash_position + (indx-price_at_change) * -stock_position

            records.append((month_year, net_worth, benchmark_stock_position * indx))

with open("backtest.csv", "w") as f:
    w = csv.writer(f)
    w.writerow(["Date","Net Worth", "All Long Net Worth"])
    w.writerows(records)