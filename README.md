# NLP-Sentiment-Methods

The code in this respository takes a Nasdaq news dataset and uses the text files for sentiment analysis. 

Code:

Process data - processes raw json data file to extract the date, ticker and text. Data is being sorted by Year and Isoweek. 
Word count variable is created. Text is cleaned and stemmed (optional). Date is formatted and permno is fetched for later wrds data extraction. 

Get_paneldata - Gets data for panel data regression of top 100 companies w.r.t. news frequency in the years 2015 - 2019 (not included - Abnormal return)

Merge_data - Merges data of get_paneldata.ipynb with text dataset of process_data.ipynb

GetdataAR - Gets data corresponding to abnormal return at day of news article publication

Get_dm_sentiment - Estimation of sentiment via dm methods

Get_RF_sentiment_AR - Estimation of sentiment via random forest 

BERT_finetuning - Fine-tuning of BERT for classification task 
