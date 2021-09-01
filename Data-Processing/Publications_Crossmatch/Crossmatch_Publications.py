import numpy as np
from astropy import units as u
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord
import pandas as pd

df = pd.read_csv('Crossmatch_AB.csv')   #A catalog
f = pd.read_csv('Publications_Updated.csv') #B catalog

ra_A = df['ra']
dec_A = df['dec']
ra_B = f['ra']
dec_B = f['dec']

sourcecat = SkyCoord(ra = ra_A*u.degree, dec=dec_A*u.degree, frame='icrs')
astrocat = SkyCoord(ra = ra_B*u.degree, dec=dec_B*u.degree, frame='icrs')

idx,d2d,d3d = (sourcecat).match_to_catalog_sky(astrocat)  #crossmatch
max_radius = 120./3600 #120 arcsec 

df['Publications_Flag'] = np.zeros(len(df))
df['Publications'] = np.zeros(len(df))

Required_Types = list(['LMXB','HMXB','LPV*','GlCl','EB*','XB','Be*','Symbiotic*']) #only sources of this type will be crossmatched to avoid errors

for id1, (closest_id2, dist) in enumerate(zip(idx, d2d)):
    closest_dist = dist.value
      
    if closest_dist < max_radius:
        if f['Source_Type'][closest_id2] in Required_Types:         
            df['Publications_Flag'][id1] = 1 #Set Flag = 1 if there is a match
            df['Publications'][id1] = f['Publications'][closest_id2]

    else:
        pass

print(df.head())
df.to_csv('Complete_Catalog.csv', index=False)
