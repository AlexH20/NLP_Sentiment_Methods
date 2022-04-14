import csv
import sys
import pandas as pd
import json

#To max out field limit
csv.field_size_limit(sys.maxsize)

#The following code extracts date, ticker and text from the json file in the NASDAQ data folder and creates a csv file with the three columns

json_file_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/Nasdaq/NASDAQ_News.json"
first_csv_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/data_compact.csv"

with open(json_file_path, 'r') as json_file:
    with open(first_csv_path, 'w') as first_csv:
        writer = csv.writer(first_csv)
        writer.writerow(["Date", "Ticker", "Text"])
        for i, line in enumerate(json_file):
            data = json.loads(line)

            try:
                writer.writerow([data["article_time"]["$date"], data["symbols"], data["article_content"]])
            except KeyError:
                continue

            if i == 100:
                break

        json_file.close()
        first_csv.close()


#The following code takes the csv file created from the code above and adjusts the date format such that it can be used to fetch data from the wrds database

csv_processed_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/data_compact_processed.csv"

#Open file to read and one to write
with open(first_csv_path, newline='') as first_csv:
    with open(csv_processed_path, "w") as csv_processed:

        nasdaq_news = csv.reader(first_csv)

        writer = csv.writer(csv_processed)
        writer.writerow(["Date", "Ticker", "Text"])

        # Skip header
        next(nasdaq_news, None)

        for news in nasdaq_news:
            # Get rid of data without ticker symbol
            if news[1] != "":

                #Change date to proper format without T and Z
                news[0] = list(news[0])
                news[0] = [w.replace("T", " ") for w in news[0]]
                news[0] = [w.replace("Z", " ") for w in news[0]]
                news[0] = "".join(news[0])
                news[0] = news[0].split(" ")[0]

                #If multiple tickers use first entry. IMPORTANT: adjust later so that file multiple tickers same text
                news[1] = news[1].split(sep= ",")[0]

                writer.writerow([news[0], news[1], news[2]])

        first_csv.close()
        csv_processed.close()

#Open newly created csv file in read mode which contains tickers
df = pd.read_csv(csv_processed_path)

txtticker_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/data_compact_ticker.txt"

#Write txt file as file document supported on wrds database with txt ticker names to get permno to upload on wrds to get permnos as csv (select only latest permnos):https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/tools/translate-to-permcopermno/
with open(txtticker_path, "w") as f:
    for index, row in df.iterrows():
        f.write(str(row["Ticker"]) + "\n")






