import numpy as np
import pandas as pd



df = pd.read_csv("boliga_data_being_sold.csv")

'''
df = pd.concat([old_df,new_df])
df = df.dropna()
df = df.drop_duplicates(subset='url')
df.to_csv("boliga_data_sold_sorted.csv")

'''

print(len(df))

df = df.drop_duplicates('url', keep='last')

print(len(df))