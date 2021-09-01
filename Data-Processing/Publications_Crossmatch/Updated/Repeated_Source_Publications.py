import numpy as np
import pandas as pd 
from astropy import units as u
from astroquery.simbad import Simbad
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord

df = pd.read_csv('Publications_With_Coordinates.csv')
df = df[df['SIMBAD_Name'] != '0.0']
df = df.drop_duplicates(subset=['SIMBAD_Name', 'Publications'], keep='first')

df_new = df.groupby(['SIMBAD_Name'])['Publications'].apply(','.join).reset_index()
df_new = df_new.sort_values(by=['SIMBAD_Name']).reset_index()

df = df.drop_duplicates(subset=['SIMBAD_Name'], keep='first')
df = df.sort_values(by=['SIMBAD_Name']).reset_index(drop=True)
df['Publications'] = df_new['Publications']

print(df.head())
df.to_csv('Publications_Updated.csv', index=False)
