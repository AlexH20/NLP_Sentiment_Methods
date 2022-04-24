import wrds
import csv
from datetime import datetime, timedelta
import sys
import numpy as np
import statsmodels.formula.api as sm
import pandas as pd
import os
from time import time

#To max out field limit
csv.field_size_limit(sys.maxsize)

db = wrds.Connection(wrds_username='holzeral')

input_file_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/"
input_file_name = "sorted_processed_data.csv"
output_file_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/"
output_file_name = "sorted_data_wcontrol.csv"


data = pd.read_csv(input_file_path + input_file_name)
data_fill = []

for index, row in data.iterrows():

    permno = row["Permno"]
    ticker = row["Ticker"]
    print(ticker)

    # Change string to datetime. Disregard H/M/S for control variables
    date = row["Date"].split(" ")[0]
    date = datetime.strptime(date, "%Y-%m-%d")

    ########## Following code uses wrds database to extract data for control variable: share turnover and nasdaq dummy ##########

    # Substract days from datetime variable to get start and end date in API request
    day0 = date - timedelta(0)
    dayminus1 = date - timedelta(1)
    dayminus252 = date - timedelta(252)
    dayminus6 = date - timedelta(6)

    # Convert to proper time format for wrds request
    day0 = day0.strftime("%m/%d/%Y")
    dayminus1 = dayminus1.strftime("%m/%d/%Y")
    dayminus6 = dayminus6.strftime("%m/%d/%Y")
    dayminus252 = dayminus252.strftime("%m/%d/%Y")

    # data query to get control variable share turnover: volume within (-252,-6) divided by shares outstanding on 0
    voldata = db.raw_sql("""select permno, vol 
                                    from crsp.dsf
                                    where permno = {}
                                    and date between '{}' and '{}'""".format(permno, dayminus252, dayminus6))

    shrout_m1 = db.raw_sql("""select shrout
                                    from crsp.dsf
                                    where permno = {}
                                    and date = '{}'""".format(permno, day0))

    # Fetch nasdaq issue number
    issuno = db.raw_sql("""select issuno
                                            from crsp.dsf
                                            where permno = {}
                                            and date = '{}'""".format(permno, dayminus1))

    # Nasdaq dummy: 1 if Nasdaq number != 0. Try and except to circumvent empty pd.series convert problem if no data fetched
    try:
        if int(issuno["issuno"]) != 0:
            issuno_i = 1
        else:
            issuno_i = 0
    except TypeError:
        issuno_i = 0

    # Check if more than 60 observations of volume for date range (-252,-6)
    if len(voldata["vol"]) >= 60:
        try:
            # Shrout multiplied by 1000 because in thousands
            shareturnover = (int(voldata["vol"].sum()) / (int(shrout_m1["shrout"][0]) * 1000))
        except:
            continue
    else:
        continue

    ########## Following code uses wrds database to extract data for control variable: size  ##########

    # Size defined as price * shrout on date -1
    price_and_shroutm1 = db.raw_sql("""select prc, shrout
                                            from crsp.dsf
                                            where permno = {}
                                            and date = '{}'""".format(permno, dayminus1))

    # TypeError (None) and Indexerror (empty DF) exception for permno without data
    try:
        size = price_and_shroutm1["prc"][0] * int(price_and_shroutm1["shrout"][0])
    except (TypeError, IndexError):
        continue

    ########## Following code uses wrds database to extract data for control variable: size  ##########

    # Get date one year ago to set range in SQL request
    dayminus365 = date - timedelta(365)
    dayminus365 = dayminus365.strftime("%m/%d/%Y")

    assets_and_equity = db.raw_sql("""select tic, act, seq
                                            from comp.funda
                                            where tic = '{}'
                                            and datadate between '{}' and '{}'""".format(ticker, dayminus365, day0))

    # BTM defined as Assets / Market value of firm, where Market value of firm = Assets - Book Equity (Stockholders Equity) + Market Equity (Shrout * Prc) (Fama and French 2001)
    # TypeError (None) and Indexerror (empty DF) exception for ticker symbols who don't have assets or liabilities

    try:
        # Assets are in millions and size in thousands. Therefore size gets divided by 1000
        btm = \
            (assets_and_equity["act"] / (assets_and_equity["act"][0] - assets_and_equity["seq"][0] + (size / 1000)))[0]
    except (TypeError, IndexError):
        continue

    ########## Following code uses wrds database to extract data for control variable: pref_alpha  ##########

    ret = db.raw_sql("""select date, ret 
                                                        from crsp.dsf
                                                        where permno = {}
                                                        and date between '{}' and '{}'""".format(permno, dayminus252,
                                                                                                 dayminus6))

    ff = db.raw_sql("""select date, mktrf, smb, hml, rf
                                                        from ff.factors_daily
                                                        where date between '{}' and '{}'""".format(dayminus252,
                                                                                                   dayminus6))

    # Change fetched data to pandas dataframe
    ff = pd.DataFrame(ff, columns=["date", "mktrf", "smb", "hml", "rf"])
    ret = pd.DataFrame(ret, columns=["date", "ret"])

    # Merge the two dataframes on date and drop NAs so only dates with no missing values are included in the regression
    data = ret.merge(ff,
                     on="date",
                     how="left")

    data = data[data.notna()]

    # Substract risk free rate from daily return to get excess return
    data["excess_return"] = data["ret"] - data["rf"]
    data_reg = data.drop(["rf", "date"], axis=1)

    # At least 60 daily returns must be available to be included in the sample (Loughran and McDonald 2011)
    if (len(data)) >= 60:
        # Regression of Fama and French 3 factor model to estimate pref_alpha (Intercept)
        model = sm.ols("excess_return ~ mktrf + smb + hml", data=data_reg).fit()
        pre_falpha = model.params["Intercept"]
    else:
        continue

    ########## Following code uses wrds database to extract data for dependent variable: excess returns day period: 0 to 3  ##########
    # Excess return defined as 4 day period buy and hold return from day 0 to day 3 minus cumul value weighted CRSP return in this period

    # Last day of buy and hold period
    dayplus3 = date + timedelta(3)
    dayplus3 = dayplus3.strftime("%m/%d/%Y")

    # Fetch prices and returns for given buy and hold period
    exc_ret = db.raw_sql("""select date, prc, ret
                                            from crsp.dsf
                                            where permno = {}
                                            and date between '{}' and '{}'""".format(permno, dayminus1, dayplus3))

    vw_ret = db.raw_sql("""select date, vwretd
                                            from crsp.dsi
                                            where date between '{}' and '{}'""".format(dayminus1, dayplus3))

    # Initialize cumulative return variable to 1, as we need to multiply returns of each given day in the buy and hold period
    cumul_return = 1
    vw_cumul_return = 1
    for i in range(len(exc_ret["ret"]) - 1):
        cumul_return *= (1 + exc_ret["ret"][i])
        vw_cumul_return *= (1 + vw_ret["vwretd"][i])
    cum_ab_return = cumul_return - vw_cumul_return

    data_fill.append([date, ticker, row["Text"], row["Word Count"], row["Permno"], row["Year"], row["Week"], issuno_i, shareturnover, size, btm, pre_falpha, cum_ab_return])

df = pd.DataFrame(data_fill, columns = ["Date", "Ticker", "Text", "Word Count", "Permno", "Year", "Week", "Nasdaq", "Turnover", "Size", "BTM", "pref_alpha", "CAR"])

with open(output_file_path + output_file_name, "w") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Date", "Ticker", "Text", "Word Count", "Permno", "Year", "Week", "Nasdaq", "Turnover", "Size", "BTM", "pref_alpha", "CAR"])
    for index, row in df.iterrows():
        writer.writerow(row)













