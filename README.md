# NLP-Sentiment-Methods

The code in this respository takes a Nasdaq news dataset and uses the text files for sentiment disclosure analysis. 

Code:

Process data - processes raw json data file to extract the date, ticker and text. Data is being sorted by Year and Isoweek. 
Word count variable is created. Text is cleaned and stemmed (optional). Date is formatted and permno is fetched for later wrds data extraction. 

Descriptive statistics - code to get an overview over the data

Fetch_data_wrds - fetches controls and dependent variable from wrds

Get_dm_sentiment - code to extract sentiment according to LM and HIV$

ML_ngrams - code to extract sentiment via ML RF ngram approach


Steps missing: 

word embedding,
word embedding used with neural nets and rf,
linear regression with control variables and sentiment measures on CAR
