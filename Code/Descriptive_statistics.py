import pandas as pd
import pysentiment2 as ps

#Get data from file path
input_file_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/descriptive data/"
input_file_name = "sorted_processed_data.csv"
data = pd.read_csv(input_file_path + input_file_name, index_col= False)

#Prepare data for descriptive statistics
data["Date"] = pd.to_datetime(data["Date"], format = "%Y-%m-%d")

#Function to split initial dataframe into dataframes grouped by year
def split_years(dt):
    dt["Year"] = dt["Date"].dt.year
    return [dt[dt["Year"] == y] for y in dt["Year"].unique()]

data_splt_years = split_years(data)
data_fill = []

for df_year_splt in data_splt_years:
    year = df_year_splt["Date"].iloc[0].year
    obs_count = len(df_year_splt)
    earliest_obs = df_year_splt["Date"].iloc[0]
    latest_obs = df_year_splt["Date"].iloc[-1]
    mean_word_count = df_year_splt["Word Count"].mean()
    company_count = df_year_splt["Ticker"].nunique()

    data_fill.append([year, obs_count, earliest_obs, latest_obs, mean_word_count, company_count])

#Calculate the metrics for the whole dataset
obs_count = len(data)
earliest_obs = data["Date"].iloc[0]
latest_obs = data["Date"].iloc[-1]
mean_word_count = data["Word Count"].mean()
company_count = data["Ticker"].nunique()

data_fill.append(["All years", obs_count, earliest_obs, latest_obs, mean_word_count, company_count])

df_by_year = pd.DataFrame(data_fill ,columns = ["Year", "Observations", "Earliest Observation", "Latest Observation", "Mean Word Count", "Company Count"])

print(df_by_year)

#Get an overview of the data with respect to the companies

unique_data_company =  data.groupby("Ticker").nunique().sort_values(by = ["Date", "Year"], ascending = [False, False])
df_unique_data_company = pd.DataFrame(unique_data_company, columns = ["Date", "Text", "Word_count", "Year"])

del df_unique_data_company["Word_count"]
df_unique_data_company.rename(columns={"Text":"News Articles"}, inplace=True)
df_unique_data_company["Average Articles p.d."] = round(df_unique_data_company["News Articles"] / data["Date"].nunique(), 2)

print(df_unique_data_company)

#Get an overview on how many companies and news in each week

print(data.groupby(["Year", "Week"])["Ticker"].nunique())
print(data.groupby(["Year", "Week"])["Text"].nunique())

"""#Sentiment indices description using DM methods.

hiv4 = ps.HIV4()
lm = ps.LM()

data_fill = []

for df_year_splt in data_splt_years:

    year = df_year_splt["Date"].iloc[0].year

    hiv4_pos = []
    hiv4_neg = []
    hiv4_tone = []

    lm_pos = []
    lm_neg = []
    lm_tone = []

    for index, row in df_year_splt.iterrows():

        tokens_hiv4 = hiv4.tokenize(row["Text"])
        tokens_lm = lm.tokenize(row["Text"])

        score_hiv4 = hiv4.get_score(tokens_hiv4)
        score_lm = lm.get_score(tokens_lm)

        hiv4_pos.append(score_hiv4["Positive"])
        hiv4_neg.append(score_hiv4["Negative"])
        hiv4_tone.append(score_hiv4["Positive"] - score_hiv4["Negative"])

        lm_pos.append(score_lm["Positive"])
        lm_neg.append(score_lm["Negative"])
        lm_tone.append(score_lm["Positive"] - score_lm["Negative"])

    data_fill.append([year, sum(hiv4_pos), sum(hiv4_neg), sum(hiv4_tone), sum(lm_pos), sum(lm_neg), sum(lm_tone)])

df_by_year_dm = pd.DataFrame(data_fill ,columns = ["Year", "HIV4 positive", "HIV4 negative", "HIV4 tone", "LM_pos", "LM_neg", "LM_tone"])

df_by_year_dm.loc["Total"] = df_by_year_dm.sum(numeric_only=True, axis = 0)
df_by_year_dm.at["Total", "Year"] = "All years"

print(df_by_year_dm)"""




