import numpy as np
import pandas as pd 
from astropy import units as u
from astroquery.simbad import Simbad
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord

Simbad.add_votable_fields('otype')
Simbad.TIMEOUT = 200

df = pd.read_csv('Hcat.csv') #Catalog of High/Low Mass Binaries
df['Flag'] = np.zeros((len(df)))

for i in range(len(df)):

    if df['Object Type'][i] == 'LMXB':
        df['Flag'][i] = 1
    elif df['Object Type'][i] == 'HMXB':
        df['Flag'][i] = 1
    elif df['Object Type'][i] == 'EB*':
        df['Flag'][i] = 1
    elif df['Object Type'][i] == 'LPV*':
        df['Flag'][i] = 1
    elif df['Object Type'][i] == 'Symbiotic*':
        df['Flag'][i] = 1

ra = df['ra']
dec = df['dec']
df['New_Name'] = np.zeros(len(df))
df['New_Type'] = np.zeros(len(df))


for i in range(len(df)): #If the nearest source is not a binary, match it to the nearest HMXB/LMXB within 10arcmin
    if df['Flag'][i] == 0:

        result_table = Simbad.query_region(coord.SkyCoord(ra[i], dec[i], unit=(u.deg, u.deg), frame='icrs'), radius='0d10m0s')

        if result_table:
            print(i)

            for j in range(len(result_table)):
                if result_table['OTYPE'][j].decode("utf-8") == 'LMXB':
                    df['New_Name'][i] = result_table['MAIN_ID'][j].decode("utf-8")
                    df['New_Type'][i] = result_table['OTYPE'][j].decode("utf-8")
                    break;
            
                elif result_table['OTYPE'][j].decode("utf-8") == 'HMXB':
                    df['New_Name'][i] = result_table['MAIN_ID'][j].decode("utf-8")
                    df['New_Type'][i] = result_table['OTYPE'][j].decode("utf-8")
                    break;

                elif result_table['OTYPE'][j].decode("utf-8") == 'LPV*':
                    df['New_Name'][i] = result_table['MAIN_ID'][j].decode("utf-8")
                    df['New_Type'][i] = result_table['OTYPE'][j].decode("utf-8")
                    break;

                elif result_table['OTYPE'][j].decode("utf-8") == 'EB*':
                    df['New_Name'][i] = result_table['MAIN_ID'][j].decode("utf-8")
                    df['New_Type'][i] = result_table['OTYPE'][j].decode("utf-8")
                    break;
                

print(df.head())
df.to_csv('Hcat.csv', index=None) 
