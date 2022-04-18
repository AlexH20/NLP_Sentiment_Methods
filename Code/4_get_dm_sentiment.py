import csv
import pysentiment2 as ps


input_file_path = "INPUT FILE PATH"
output_file_path = "OUTPUT FILE PATH"

with open(input_file_path, newline='') as csvfile:
    with open(output_file_path + "data_processed_wcontroldm", "w") as newfile:

        data_reader = csv.reader(csvfile)
        writer = csv.writer(newfile)
        writer.writerow(["date" , "ticker", "text", "nasdaq_dummy", "share_turnover", "size", "BTM", "pref_alpha", "cum_ab_ret", "hiv4_neg", "hiv4_pos", "hiv4_tone", "lm_neg", "lm_pos", "lm_net"])

        #Initial dictionary methods. Harvard and LM dms will be used to assess text sentiment
        hiv4 = ps.HIV4()
        lm = ps.LM()

        # Skip header
        next(data_reader, None)

        #Use texts in csv file to tokenize and get counts of positive and negative words according to HIV4 and LM
        for values in data_reader:

            text = values[2]

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

            writer.writerow([values[0] ,values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], hiv4_neg, hiv4_pos, hiv4_tone, lm_neg, lm_pos, lm_tone])






