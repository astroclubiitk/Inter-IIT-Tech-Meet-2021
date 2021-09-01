import pandas as pd

df = pd.read_csv("publications-list.csv")
df = df.drop(['Authors'], axis = 1) 
df =df.drop(['Keywords'], axis = 1) 
df =df.drop(['Abstract'], axis = 1)
print(df) 

df.to_csv('publications-list-final.csv')