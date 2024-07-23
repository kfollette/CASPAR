#Connect to your Google Drive
from google.colab import drive
drive.mount('/content/drive')

#Import the RA and DEC Conversion Module from your Google Drive (update the path accordingly)
import sys
sys.path.append('/content/drive/My Drive/')
import RA_DEC_Converter

#Import other useful modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import scipy.stats as st
import scipy.optimize as opt
from astropy import units as u
from astropy.coordinates import SkyCoord
import seaborn as sb
from sklearn.neighbors import KernelDensity
from scipy.stats import gaussian_kde

#Install AstroQuery
!pip install astroquery
from astroquery.gaia import Gaia as g
from astroquery.simbad import Simbad

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#Set data source to DR3 Archive (Can also be set to DR2)
g.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"

#Set object limit (For an unlimited number of objects, set g.ROW_LIMIT to -1)
g.ROW_LIMIT = 

#Input the RA and DEC of a region from SIMBAD (RAhr, RAmin, RAsec, DEChr, DECmin, DECsec)
ra_dec = RA_DEC_Converter.degcon()

#Use the computed RA and DEC to set the coordinates of the region
coord = SkyCoord(ra=ra_dec[0], dec=ra_dec[1], unit=(u.degree, u.degree), frame='icrs')

#Set the radius of search (Can also be set to arsec and arcmin)
rad = u.Quantity(, u.deg)

#Search GAIA database for stars within the inputted radius of the region
z = g.cone_search_async(coord, radius = rad, columns = ['SOURCE_ID', 'ra', 'dec', 'parallax','parallax_error', 'pmra', 'pmra_error', 'pmdec', 'pmdec_error', 'radial_velocity'])
r = z.get_results()

#Convert to a pandas data table with the desired columns from the GAIA output
new_gaia = pd.DataFrame({'SOURCE_ID':r['SOURCE_ID'], 'RA (J2016.0)':r['ra'], 'DEC (J2016.0)': r['dec'], 'Parallax': r['parallax'], 'Parallax err': r['parallax_error'], 'RA proper motion': r['pmra'], 'RA proper motion err': r['pmra_error'], 'DEC proper motion': r['pmdec'], 'DEC proper motion err': r['pmdec_error'], 'Radial Velocity': r['radial_velocity']})

#Input the GAIA DR3 Source ID into the SIMBAD Query to get object names ('MAIN_ID')
i = 0
b = []
c = []

while i < len(new_gaia):
  b = (Simbad.query_object("Gaia DR3 " + str(new_gaia['SOURCE_ID'][i])))
  
  if b is not None:
   c.append(((new_gaia['SOURCE_ID'][i]), list(b['MAIN_ID']), list(b['RA']), list(b['DEC']), new_gaia['Parallax'][i], new_gaia['Parallax err'][i], new_gaia['RA proper motion'][i],  new_gaia['RA proper motion err'][i],  new_gaia['DEC proper motion'][i],  new_gaia['DEC proper motion err'][i],  new_gaia['Radial Velocity'][i]))
  
  i+=1

c2 = pd.DataFrame(c)
c2.columns = ['SOURCE_ID', 'MAIN_ID', 'RA (J2000.0)', 'DEC (J2000.0)', 'Parallax', 'Parallax err', 'RA proper motion', 'RA proper motion err', 'DEC proper motion', 'DEC proper motion err', 'Radial Velocity']

#Remove the brackets that show up around the outputs
c2['RA (J2000.0)'] = c2['RA (J2000.0)'].str[0]
c2['DEC (J2000.0)'] = c2['DEC (J2000.0)'].str[0]
c2['MAIN_ID'] = c2['MAIN_ID'].str[0]

c2




