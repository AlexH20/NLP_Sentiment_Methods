# NLP-Sentiment-Methods

The code in this respository takes a Nasdaq news dataset and uses the text files for sentiment disclosure analysis. 

Steps:

1)The code 1_process_data.py takes a json file as input and returns a csv file in the chosen path with three columns (Date, Ticker and Text) 
and a .txt file with the ticker names.

2)The .txt file needs to be uploaded in the wrds CRSP database https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/tools/translate-to-permcopermno/
to retrieve a csv file with the latest permnos of the associated ticker names, which will be used to fetch the dependent variable and control variables.

3)The code 2_merge_permno_with_csv.py merges the permno csv file from the step above with the csv file created in step 1) 
which returns a csv file (columns: ['Date', 'Ticker', 'Text', 'Date_Permno', 'Permno']).

4)3_fetch_data_wrds.py takes the csv file from step 3), fetches financial data from wrds and returns a csv file with the control variables and 
the dependent variable CAR (columns: ["date", "ticker", "text", "nasdaq_dummy", "share_turnover", "size", "BTM", "pref_alpha", "cum_ab_ret"])

5)4_get_dm_sentiment.py takes the file from step 4) and adds with the help of the pysentiment2 library the negative, positive and tone (positive - negative)
count according to the LM and HIV4 dictionaries for unsupervised sentiment disclosure analysis.
(additional columns: ["hiv4_neg", "hiv4_pos", "hiv4_tone", "lm_neg", "lm_pos", "lm_net"]).

6)5_get_ngrams.py takes as inputs the training and test datasets and creates sparse matrices with a structure according to the one- and two grams
found in the training dataset. These sparse matrices with the dependent variable CAR (cumulative abnormal returns) can be used to train and test
random forest classifiers. 


Steps missing: 

word embedding
word embedding used with neural nets and rf
linear regression with control variables and sentiment measures on CAR
