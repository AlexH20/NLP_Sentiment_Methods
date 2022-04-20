import csv
import sys
import pandas as pd
import json
import os
import re
import string
from nltk.stem.porter import *
from datetime import datetime
stemmer = PorterStemmer()
exclude = set(string.punctuation)

#To max out field limit
csv.field_size_limit(sys.maxsize)

#The following code extracts date, ticker and text from the json file in the NASDAQ data folder and creates a csv file with the three columns
#Additionally it takes the json file data created and adjusts the date format such that it can be used to fetch data from the wrds database
#The text will be processed to reduce noise with the help of the functions from Frankel, Jennings and Lee (2021)

#### FUNCTIONS TO CLEAN PHRASES AND WORDS #### Frankel, Jennings and Lee (2021)

stopwords = ['a','able','across','after','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','let','like','likely','me','my','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your']

stopwords_dict={}
for stopword in stopwords:
    stopwords_dict[stopword]=0

def fix_phrases(section):
    section = re.sub('(\d+)\.(\d+)','\g<1>\g<2>',section) # Remove periods from numbers -- 4.55 --> 455
    section = section.replace(".com", "com")
    section = section.replace("-", " ")
    section = section.replace('. .', '.')
    section = section.replace('.', 'XXYYZZ1')
    section = ''.join(ch for ch in section if ch not in exclude) #Delete all punctuation except periods
    section = section.replace('XXYYZZ1', '.')
    section = section.lower()
    section = re.sub(' +',' ',section) #Remove multiple spaces
    if section == '.': section = ''
    return section

def fixword(word, portstem = True):
        word = word.replace('\n','')
        if re.search('[0-9]',word) != None:
            word = '00NUMBER00' # Replace numbers with 000NUMBER000
        try:
            test = stopwords_dict[word]
            word = '_' # Replace stop words with _
        except Exception:
            donothing = 1
        #Variable if stemming or not
        if portstem:
            try:
                word = stemmer.stem(word)  # Stemp words
            except Exception:
                word = ''
        return word

json_file_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/Nasdaq/NASDAQ_News.json"
output_file_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/"

with open(json_file_path, 'r') as json_file:
    with open(output_file_path + "data_processed.csv", "w") as csv_file:

        writer = csv.writer(csv_file)
        writer.writerow(["Date", "Ticker", "Text", "Word_count"])

        for i, line in enumerate(json_file):

            data = json.loads(line)

            try:
                date = data["article_time"]["$date"]
            except KeyError:
                continue

            try:
                ticker = data["symbols"]
            except KeyError:
                continue

            try:
                text = data["article_content"]
            except KeyError:
                continue

            if len(ticker.split(sep=",")) == 1 and ticker != "":

                print(ticker)

                # Change date to proper format without T and Z
                date = list(date)
                date = [w.replace("T", " ") for w in date]
                date = [w.replace("Z", " ") for w in date]
                date = "".join(date)
                date = pd.to_datetime(date.split(" ")[0])

                # If multiple tickers use first entry. IMPORTANT: adjust later so that file multiple tickers same text
                ticker = ticker.split(sep=",")[0]

                # Pre-processing text to reduce noise and prepare text data for word representation techniques (word embedding). Part of the code is taken from Frankel, Jennings and Lee (2021)
                text = fix_phrases(text)
                sentences = text.split('.')

                count_words = 0

                for v, sentence in enumerate(sentences):

                    sentences[v] = sentences[v].replace(".", "").strip()

                    allwords = sentences[v].split(" ")

                    for w, word in enumerate(allwords):
                        count_words += 1
                        allwords[w] = fixword(allwords[w])

                    sentences[v] = " ".join(allwords)

                text = ".".join(sentences)

                writer.writerow([date.strftime("%Y-%m-%d"), ticker, text, count_words])

        json_file.close()


txtticker_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/"

#Write txt file as file document supported on wrds database with txt ticker names to get permno to upload on wrds to get permnos as csv (select only latest permnos):https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/tools/translate-to-permcopermno/
with open(txtticker_path + "dataticker.txt", "w") as f:
    for index, row in df.iterrows():
          f.write(str(row["Ticker"]) + "\n")









