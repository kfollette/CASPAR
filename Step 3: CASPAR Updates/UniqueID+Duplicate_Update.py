pip install --pre astroquery

import numpy as np
%matplotlib inline
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from astroquery.simbad import Simbad
from tqdm import tqdm

from google.colab import drive
drive.mount('/content/drive')
CASPAR = pd.read_csv('/content/drive/MyDrive/Code/Code_Files/caspar_copy.csv', skiprows=1)
#Below gets rid of units column, for doing comparisons and searches to avoid errors
CASPAR.drop(index=0,inplace=True)
CASPAR.reset_index(drop=True,inplace=True)

#make list of unique simbad names for query input
caspar_unique = CASPAR.drop_duplicates('Simbad-Resolvable Name').reset_index()
simbad_names = caspar_unique['Simbad-Resolvable Name'].to_list()

def query(SimbadName):
  try:
    #query names associated with input
    result_table = Simbad.query_objectids(SimbadName)
    #put names in list
    result_list = result_table.columns[0].tolist()
    try:
      #find 2MASS in list of strings and pull out to return
      result = [name for name in result_list if '2MASS ' in name][0] #space needed after 2MASS so to not catch 2MASSs
      return result
    except IndexError: #inputs that return no 2MASS name
      return 'No 2MASS name'
  except AttributeError: #inputs that don't get recognized by SIMBAD
    return 'No input found in SIMBAD'

    #dictionary with key as input and value as 2mass return
d = {}
for name in tqdm(simbad_names):
  d[name] = query(name)

  #make new column for unique ids at start of df
CASPAR.insert(0,'Unique Name',value=['' for i in range(len(CASPAR))])

#Append unique ids to CASPAR, use simbad if no 2mass
for ind in CASPAR.index:
  if d[CASPAR.loc[ind,'Simbad-Resolvable Name']] == 'No 2MASS name':
    CASPAR.loc[ind,'Unique Name'] = CASPAR.loc[ind,'Simbad-Resolvable Name']
  elif d[CASPAR.loc[ind,'Simbad-Resolvable Name']] == 'No input found in SIMBAD':
    CASPAR.loc[ind,'Unique Name'] = CASPAR.loc[ind,'Simbad-Resolvable Name']
  else:
    CASPAR.loc[ind,'Unique Name'] = d[CASPAR.loc[ind,'Simbad-Resolvable Name']]
  #remove NAME if present
  if CASPAR.loc[ind,'Unique Name'][:5] == 'NAME ':
    CASPAR.loc[ind,'Unique Name'] = CASPAR.loc[ind,'Unique Name'][5:]

#make 2 new columns in CASPAR
CASPAR['Duplicate #'] = ''
CASPAR['Total Duplicates'] = ''

#make dataframe with name and # of duplicates for each unique name (size)
dups = CASPAR.groupby('Unique Name', as_index=False).size()
#populate Nduplicates in CASPAR
for ind in dups.index:
  name = dups.loc[ind,'Unique Name']
  CASPAR.loc[CASPAR['Unique Name'] == name, 'Total Duplicates'] = dups.loc[ind,'size']

  #make series holding unique object names
names = CASPAR['Unique Name'].drop_duplicates()
#make duplicate dataframe to sort
caspar_sorted = pd.DataFrame(columns=CASPAR.columns)
#for each unique name, find where it shows up in original and sort those by epoch, append to duplicate dataframe
for i in names:
  caspar_sorted = caspar_sorted.append(CASPAR[CASPAR['Unique Name'] == i].sort_values('Epoch'))
#result is alphabetized Simbad names with subcategory sorting by epoch
caspar_new = caspar_sorted.reset_index()

counter = 1
#check ind+1 to see if neighbour has same name, if so count and use counter as n/N
for ind in np.arange(0,len(caspar_new)): #-1 to prevent index out of bounds at the end of the dataframe
  try:
    caspar_new.loc[ind,'Duplicate #'] = str(counter)
    check_neighbour = caspar_new.loc[ind,'Unique Name'] == caspar_new.loc[ind+1,'Unique Name']
    if check_neighbour:
      counter += 1
    else:
      counter = 1
  except KeyError:
    print('reached end, no further indexing')
    #caspar_sorted.loc[ind,'Nduplicates'] = str(counter) + '/' + str(caspar_sorted.loc[ind,'Nduplicates'])

    caspar_new.to_excel('/content/drive/MyDrive/Code/Code_Files/Output/caspar_new.xlsx')
