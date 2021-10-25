import numpy as np
import pandas as pd


old_df = pd.read_csv("boliga_data_sold2.csv")
new_df = pd.read_csv("boliga_data_sold.csv")

df = pd.concat([old_df,new_df])
df = df.dropna()
df = df.drop_duplicates(subset='url')
df.to_csv("boliga_data_sold_sorted.csv")