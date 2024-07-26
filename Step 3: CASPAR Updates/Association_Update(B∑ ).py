!pip install astropy
import numpy as np
import math
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from tqdm import tqdm

from google.colab import drive
drive.mount('/content/drive')
AgeSheet = pd.read_excel('/content/drive/MyDrive/CASPAR/Summer 2021 Work/BANYAN∑/SFR DATA.xlsx', sheet_name='Age Sheet')
AgeSheet.drop(index=0,inplace=True)
AgeSheet.reset_index(drop=True,inplace=True)
CASPAR = pd.read_excel('/content/drive/MyDrive/CASPAR/CASPAR_excel.xlsx',sheet_name='CASPAR',skiprows=1)
CASPAR.drop(index=0,inplace=True)
CASPAR.reset_index(drop=True,inplace=True)
BanyanResults = pd.read_excel('/content/drive/MyDrive/CASPAR/Summer 2021 Work/BANYAN∑/SFR DATA.xlsx', sheet_name='Banyan Results')
BanyanResults.reset_index(drop=True,inplace=True)

BanyanResults = BanyanResults.sort_values('Name').reset_index().drop(columns='index')
CASPAR_unique = CASPAR.sort_values('Unique Name').drop_duplicates('Unique Name').reset_index().drop(columns='index')
len(CASPAR_unique)
len(BanyanResults)

#confirm that both dataframes are sorted in the same way
for ind in BanyanResults.index:
  if BanyanResults.loc[ind,'Name'] == CASPAR_unique.loc[ind,'Unique Name']:
    continue
  else:
    print('Oh no!')

    #new columns for CASPAR
CASPAR['Banyan Association'] = np.nan
CASPAR['Banyan Association Probability'] = np.nan
CASPAR['Banyan Association Age'] = np.nan

for ind in BanyanResults.index:
  ya_abbr = BanyanResults.loc[ind,'Best_YA']
  ya_prob = BanyanResults.loc[ind,'YA prob.']
  field_prob = BanyanResults.loc[ind,'Field Star prob.']
  if str(ya_abbr) == 'nan': #deal with objects that didn't run in Banyan ∑, leave as nan
    CASPAR.loc[CASPAR['Unique Name'] == BanyanResults.loc[ind,'Name'],'Banyan Association'] = np.nan
  elif field_prob > 0.5: #set as field star if above 50% probability
    CASPAR.loc[CASPAR['Unique Name'] == BanyanResults.loc[ind,'Name'],'Banyan Association'] = 'FIELD'
    CASPAR.loc[CASPAR['Unique Name'] == BanyanResults.loc[ind,'Name'],'Banyan Association Probability'] = field_prob
  else:
    try:
      #set Banyan Association in CASPAR to SFR based on AgeSheet reference
      CASPAR.loc[CASPAR['Unique Name'] == BanyanResults.loc[ind,'Name'],'Banyan Association'] = AgeSheet.loc[ya_abbr == AgeSheet['Abbr.'],'Association'].values[0]
      #add Banyan Association probability
      CASPAR.loc[CASPAR['Unique Name'] == BanyanResults.loc[ind,'Name'],'Banyan Association Probability'] = ya_prob
    except IndexError:
      print('Banyan Best_YA abbreviation result not in the AgeSheet')

      #Grab potential IC348 memebers that were identified as field stars in CASPAR
potential_IC348 = {}
for ind in CASPAR_unique.index:
  if CASPAR_unique.loc[ind,'RA (J2000.0)'] > 52 and CASPAR_unique.loc[ind,'RA (J2000.0)'] < 58:
    if CASPAR_unique.loc[ind,'Dec (J2000.0)'] > 30 and CASPAR_unique.loc[ind,'Dec (J2000.0)'] < 35:
      potential_IC348[CASPAR_unique.loc[ind,'Unique Name']] = [CASPAR_unique.loc[ind,'GAIA EDR3 Dist.'], CASPAR_unique.loc[ind,'Ref. Association']]

      #Grab potential Sigma Orionis memebers that were identified as field stars in CASPAR
potential_sOri = {}
for ind in CASPAR_unique.index:
  if CASPAR_unique.loc[ind,'RA (J2000.0)'] > 70 and CASPAR_unique.loc[ind,'RA (J2000.0)'] < 90:
    if CASPAR_unique.loc[ind,'Dec (J2000.0)'] > -15 and CASPAR_unique.loc[ind,'Dec (J2000.0)'] < 5:
      potential_sOri[CASPAR_unique.loc[ind,'Unique Name']] = [CASPAR_unique.loc[ind,'GAIA EDR3 Dist.'], CASPAR_unique.loc[ind,'Ref. Association']]

      #Grab potential Chameleon I memebers that were identified as field stars in CASPAR
potential_CHA1 = {}
for ind in CASPAR_unique.index:
  if CASPAR_unique.loc[ind,'RA (J2000.0)'] > 150 and CASPAR_unique.loc[ind,'RA (J2000.0)'] < 180:
    if CASPAR_unique.loc[ind,'Dec (J2000.0)'] > -80 and CASPAR_unique.loc[ind,'Dec (J2000.0)'] < -70:
      potential_CHA1[CASPAR_unique.loc[ind,'Unique Name']] = [CASPAR_unique.loc[ind,'GAIA EDR3 Dist.'], CASPAR_unique.loc[ind,'Ref. Association']]

      for key, value in potential_sOri.items():
  print(key,value)

  #label field stars that look like they are memebers of IC348 with *FIELD (IC348)
for key, value in potential_IC348.items():
  if str(value[0]) == 'nan': #if distance of object is nan, skip
    continue
  if value[1] != 'σ Ori': #if object was previously (pre-Banyan) identified as FIELD, skip
    continue
  CASPAR.loc[CASPAR['Unique Name'] == key,'Banyan Association'] = '*FIELD' + ' (' + value[1] + ')'

#label field stars that look like they are memebers of CHA 1 with *FIELD (IC348)
for key, value in potential_CHA1.items():
  if str(value[0]) == 'nan': #if distance of object is nan, skip
    continue
  if value[1] == 'σ Ori': #if object was previously (pre-Banyan) identified as FIELD, skip
    continue
  CASPAR.loc[CASPAR['Unique Name'] == key,'Banyan Association'] = '*FIELD' + ' (' + value[1] + ')'

#label field stars that look like they are memebers of Sigma Orionis with *FIELD (IC348)
for key, value in potential_sOri.items():
  if str(value[0]) == 'nan': #if distance of object is nan, skip
    continue
  if value[1] == 'σ Ori': #if object was previously (pre-Banyan) identified as FIELD, skip
    continue
  CASPAR.loc[CASPAR['Unique Name'] == key,'Banyan Association'] = '*FIELD' + ' (' + value[1] + ')'

  CASPAR.to_excel('/content/drive/MyDrive/CASPAR/Summer 2021 Work/BANYAN∑/Banyan_Update.xlsx')