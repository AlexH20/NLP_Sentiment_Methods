import statsmodels.formula.api as sm
import pandas as pd

filepath = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/data_compact_finaldm.csv"

df1 = pd.read_csv(filepath)

print(df1.columns)

model = sm.ols("cum_ab_ret ~ nasdaq_dummy + share_turnover + size + BTM + pref_alpha + hiv4_neg", data = df1).fit()

print(model.summary())




