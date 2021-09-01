import numpy as np
import pandas as pd 
from astropy import units as u
from astroquery.simbad import Simbad
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord
Simbad.add_votable_fields('otype')

df = pd.read_csv('source2publications.csv')
df['ra'] = np.zeros(len(df))
df['dec'] = np.zeros(len(df))
df['SIMBAD_Name'] = np.zeros(len(df))
df['Source_Type'] = np.zeros(len(df))

for i in range(len(df)):

    result_table = Simbad.query_object(df['Source'][i])
    
    if result_table:

        try:
            c = SkyCoord(result_table[0]['RA'],result_table[0]['DEC'], unit=(u.hourangle, u.deg))
            df['ra'][i] = c.ra.degree
            df['dec'][i] = c.dec.degree

        except ValueError:
            print('ERROR')

        print(i)    
        df['SIMBAD_Name'][i] = result_table['MAIN_ID'][0].decode("utf-8")
        df['Source_Type'][i] = result_table['OTYPE'][0].decode("utf-8")


print(df.head())
df.to_csv('Publications_With_Coordinates.csv', index=None)
