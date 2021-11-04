import numpy as np
import pandas as pd

main_df = pd.read_csv("boliga_data_sold_best.csv")
print(main_df.columns)
main_df = main_df.drop('Unnamed: 0',axis=1)
#df1 = pd.read_csv("boliga_data_sold_scrabed2.csv")
#df2 = pd.read_csv("boliga_data_sold_scrabed3.csv")
#df3 = pd.read_csv("boliga_data_sold_scrabed4.csv")
#df4 = pd.read_csv("boliga_data_sold_scrabed5.csv")

#main_df = pd.concat([df1,main_df])
#main_df = pd.concat([df2,main_df])
#main_df = pd.concat([df3,main_df])
#main_df = pd.concat([df4,main_df])


'''
df = pd.concat([old_df,new_df])
df = df.dropna()
df = df.drop_duplicates(subset='url')
df.to_csv("boliga_data_sold_sorted.csv")

'''

print(main_df.head())

df = main_df.drop_duplicates('url', keep='last')
main_df.to_csv("boliga_data_sold_best.csv",index=False)
#print(len(df))