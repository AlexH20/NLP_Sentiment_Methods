import csv
import sys
import pandas as pd
import json
import os
import re
import string
from nltk.stem.porter import *
stemmer = PorterStemmer()
exclude = set(string.punctuation)

#To max out field limit
csv.field_size_limit(sys.maxsize)

#The following code extracts date, ticker and text from the json file in the NASDAQ data folder and creates a csv file with the three columns

json_file_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/Nasdaq/NASDAQ_News.json"
output_file_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/"

with open(json_file_path, 'r') as json_file:
    with open(output_file_path + "data_processed_interim.csv", 'w') as first_csv:
        writer = csv.writer(first_csv)
        writer.writerow(["Date", "Ticker", "Text"])
        for i, line in enumerate(json_file):
            data = json.loads(line)

            if i % 10 == 0:
                try:
                    writer.writerow([data["article_time"]["$date"], data["symbols"], data["article_content"]])
                except KeyError:
                    continue




        json_file.close()
        first_csv.close()


#The following code takes the csv file created from the code above and adjusts the date format such that it can be used to fetch data from the wrds database
#Additionally text will be processed to reduce noise.

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

def fixword(word):
        word = word.replace('\n','')
        if re.search('[0-9]',word) != None:
            word = '00NUMBER00' # Replace numbers with 000NUMBER000
        try:
            test = stopwords_dict[word]
            word = '_' # Replace stop words with _
        except Exception:
            donothing = 1
        try:
            word = stemmer.stem(word) # Stemp words
        except Exception:
            word = ''
        return word

#Open file to read and one to write
with open(output_file_path + "data_processed_interim.csv", newline='') as first_csv:
    with open(output_file_path + "data_processed.csv", "w") as csv_processed:

        nasdaq_news = csv.reader(first_csv)

        writer = csv.writer(csv_processed)
        writer.writerow(["Date", "Ticker", "Text"])

        # Skip header
        next(nasdaq_news, None)

        for item in nasdaq_news:
            # Get rid of data without ticker symbol
            if item[1] != "":

                #Change date to proper format without T and Z
                item[0] = list(item[0])
                item[0] = [w.replace("T", " ") for w in item[0]]
                item[0] = [w.replace("Z", " ") for w in item[0]]
                item[0] = "".join(item[0])
                item[0] = item[0].split(" ")[0]

                #If multiple tickers use first entry. IMPORTANT: adjust later so that file multiple tickers same text
                item[1] = item[1].split(sep= ",")[0]

                #Pre-processing text to reduce noise and prepare text data for word representation techniques (word embedding). Part of the code is taken from Frankel, Jennings and Lee (2021)
                item[2] = fix_phrases(item[2])
                sentences = item[2].split('.')

                for v,sentence in enumerate(sentences):

                    sentences[v] = sentences[v].replace(".", "").strip()

                    allwords = sentences[v].split(" ")

                    for w, word in enumerate(allwords):
                        allwords[w] = fixword(allwords[w])

                    sentences[v] = " ".join(allwords)


                item[2] = ".".join(sentences)

                writer.writerow([item[0], item[1], item[2]])

        first_csv.close()
        csv_processed.close()

os.remove(output_file_path + "data_processed_interim.csv")

#Open newly created csv file in read mode which contains tickers
df = pd.read_csv(output_file_path + "data_processed.csv")

txtticker_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/"

#Write txt file as file document supported on wrds database with txt ticker names to get permno to upload on wrds to get permnos as csv (select only latest permnos):https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/tools/translate-to-permcopermno/
with open(txtticker_path + "dataticker.txt", "w") as f:
    for index, row in df.iterrows():
        f.write(str(row["Ticker"]) + "\n")








