import csv
import pysentiment2 as ps
import pandas as pd


input_file_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/"
input_file_name = "sorted_data_wcontrol.csv"
output_file_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/"
output_file_name = "data_dm_regression.csv"

data = pd.read_csv(input_file_path + input_file_name)

#Initial dictionary methods. Harvard and LM dms will be used to assess text sentiment
hiv4 = ps.HIV4()
lm = ps.LM()

data_fill = []

for index, row in data.iterrows():
    # Use texts in csv file to tokenize and get counts of positive and negative words according to HIV4 and LM
    text = row["Text"]

    tokens_hiv4 = hiv4.tokenize(text)
    tokens_lm = lm.tokenize(text)

    score_hiv4 = hiv4.get_score(tokens_hiv4)
    score_lm = lm.get_score(tokens_lm)

    hiv4_pos = score_hiv4["Positive"]
    hiv4_neg = score_hiv4["Negative"]
    hiv4_tone = hiv4_pos - hiv4_neg

    lm_pos = score_lm["Positive"]
    lm_neg = score_lm["Negative"]
    lm_tone = lm_pos - lm_neg

    data_fill.append([row["CAR"], row["Nasdaq"], row["Turnover"], row["Size"], row["BTM"], row["pref_alpha"], hiv4_pos, hiv4_neg, hiv4_tone, lm_pos, lm_neg, lm_tone])

df = pd.DataFrame(data_fill, columns = ["CAR", "Nasdaq", "Turnover", "Size", "BTM", "pref_alpha", "HIV4pos", "HIV4neg", "HIV4tone", "LMpos", "LMneg", "LMtone"])

with open(output_file_path + output_file_name, "w") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["CAR", "Nasdaq", "Turnover", "Size", "BTM", "pref_alpha", "HIV4pos", "HIV4neg", "HIV4tone", "LMpos", "LMneg", "LMtone"])
    for index, row in df.iterrows():
        writer.writerow(row)








