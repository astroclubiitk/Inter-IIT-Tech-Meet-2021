import numpy as np
import pandas as pd 
from astropy import units as u
from astroquery.simbad import Simbad
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord
Simbad.add_votable_fields('otype')

df = pd.read_table('AS_observations_cat_Sept2018.txt')
df = df.drop(df.columns[[0]], axis = 1, inplace = False)
df.columns = ['Date_Observed', 'Proposal_ID', 'Target_ID', 'ra', 'dec', 'Observation_ID', 'Instrument']

df['Time_Observed'] = np.zeros(len(df))

for i in range(len(df)):
    data = df['Date_Observed'][i].split(" ")
    df['Date_Observed'][i] = data[0]
    df['Time_Observed'][i] = data[1]


ra = df['ra']
dec = df['dec']
df['SIMBAD_Name'] = np.zeros(len(ra))
df['Source_Type'] = np.zeros(len(ra))

for i in range(len(ra)):

    print(i, ra[i])
    result_table = Simbad.query_region(coord.SkyCoord(ra[i], dec[i], unit=(u.deg, u.deg), frame='icrs'), radius='0d1m0s')
    
    if result_table:
        print(result_table['MAIN_ID'][0])
        df['SIMBAD_Name'][i] = result_table['MAIN_ID'][0].decode("utf-8")
        df['Source_Type'][i] = result_table['OTYPE'][0].decode("utf-8")

df.to_csv('Astrosat.csv', index=None)
print(df)
