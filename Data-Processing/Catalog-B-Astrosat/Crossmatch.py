import numpy as np
from astropy import units as u
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord
import pandas as pd

df = pd.read_csv('Binaries_Catalog.csv')   #A catalog
f = pd.read_csv('Astrosat.csv')
f = f.drop_duplicates(subset=['SIMBAD_Name'], keep='first').reset_index(drop=True) #B catalog

ra_A = df['ra']
dec_A = df['dec']
ra_B = f['ra']
dec_B = f['dec']

sourcecat = SkyCoord(ra = ra_A*u.degree, dec=dec_A*u.degree, frame='icrs')
astrocat = SkyCoord(ra = ra_B*u.degree, dec=dec_B*u.degree, frame='icrs')

idx,d2d,d3d = (sourcecat).match_to_catalog_sky(astrocat)  #crossmatch
max_radius = 120./3600 #120 arcsec 

df['Astrosat_Flag'] = np.zeros(len(df))
df['Date_Observed'] = np.zeros(len(df))
df['Time_Observed'] = np.zeros(len(df))
df['Proposal_ID'] = np.zeros(len(df))
df['Target_ID'] = np.zeros(len(df))
df['Observation_ID'] = np.zeros(len(df))
df['Instrument'] = np.zeros(len(df))

Required_Types = list(['LMXB','HMXB','LPV*','GlCl','EB*','XB','Be*','Symbiotic*']) #only sources of this type will be crossmatched to avoid errors

for id1, (closest_id2, dist) in enumerate(zip(idx, d2d)):
    closest_dist = dist.value
      
    if closest_dist < max_radius:
        if f['Source_Type'][closest_id2] in Required_Types:         
            df['Astrosat_Flag'][id1] = 1 #Set Flag = 1 if there is a match
            df['Date_Observed'][id1] = f['Date_Observed'][closest_id2]
            df['Time_Observed'][id1] = f['Time_Observed'][closest_id2]
            df['Proposal_ID'][id1] = f['Proposal_ID'][closest_id2]
            df['Target_ID'][id1] = f['Target_ID'][closest_id2]
            df['Observation_ID'][id1] = f['Observation_ID'][closest_id2]
            df['Instrument'][id1] = f['Instrument'][closest_id2]

    else:
        pass


print(df.head())
df.to_csv('Crossmatch_AB.csv', index=False)
