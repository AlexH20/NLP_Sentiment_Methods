# NLP-Sentiment-Methods

Sentiment Analysis based on NASDAQ news article dataset.

Steps:

Process data - processes raw json data file to extract the date, ticker and text. Remove duplicates, news articles with multiple related stock ticker symbols and companies without PERMNO match. Clean text for n-gram approach. 

Get_paneldata - Gets data for panel data regression of top 100 companies w.r.t. news frequency in the years 2015 - 2019. 

Merge_data - Merges data of get_paneldata.ipynb with text dataset of process_data.ipynb. Attention: Merging either based on unprocessed text OR processed text

PorterStemm_words - Get dataset from Merge_data with processed text to porter stemm words for RF application with n-grams

DM - Use Merge_data processed text data to determine sentiment based on DM methods

RF_onetwogram - Use porterstemm_words output file to estimate sentiment based on RF with one- and two-grams

RF_with_FinBERT - Use output of Merge_data file with unprocessed text to estimate sentiment with RF BERT embeddings. Same code can be used to get sentiment based on BERT encoder or FinBERT encoder. Just adjust chosen model in code!

NN_with_FinBERT - Use output of Merge_data file with unprocessed text to estimate sentiment with FinBERT + Dropout & Dense Layer.
