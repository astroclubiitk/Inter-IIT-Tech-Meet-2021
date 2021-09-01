import numpy as np
import pandas as pd 
from astropy import units as u
from astroquery.simbad import Simbad
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord

Simbad.add_votable_fields('otype')

df = pd.read_csv('Hcat.csv') #Catalog of High/Low Mass Binaries

ra = df['ra']
dec = df['dec']
df['Actual_Name'] = np.zeros(len(ra))
df['Object Type'] = np.zeros(len(ra))

for i in range(len(ra)): #Find Source Name and Type for the Nearest Source within 2 arcmin
    result_table = Simbad.query_region(coord.SkyCoord(ra[i], dec[i], unit=(u.deg, u.deg), frame='icrs'), radius='0d2m0s')
    if result_table:
        print(result_table['MAIN_ID'][0])
        df['Actual_Name'][i] = result_table['MAIN_ID'][0].decode("utf-8")
        df['Object Type'][i] = result_table['OTYPE'][0].decode("utf-8")

print(df.head())
df.to_csv('Hcat.csv', index=None) 
