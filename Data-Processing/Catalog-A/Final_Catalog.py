import numpy as np
import pandas as pd 

df = pd.read_csv('Hcat.csv')

df['Final_Names'] = np.zeros(len(df))
df['Final_Type'] = np.zeros(len(df))


for i in range(len(df)):

    if df['Flag'][i] == 1:
        df['Final_Names'][i] = df['Actual_Name'][i]
        df['Final_Type'][i] = df['Object Type'][i]

    elif df['Flag'][i] == 0:
        if df['New_Name'][i] != '0.0':
            df['Final_Names'][i] = df['New_Name'][i]
            df['Final_Type'][i] = df['New_Type'][i]

        else:
            print(i)
            print(df['Source_Name'][i])
            df['Final_Names'][i] = df['Source_Name'][i]
            df['Final_Type'][i] = 'Unknown'
        


print(df.head())
df.to_csv('HCat_final.csv', index=False)
