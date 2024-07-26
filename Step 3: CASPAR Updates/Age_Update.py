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
CASPAR = pd.read_excel('/content/drive/MyDrive/CASPAR/Summer 2021 Work/CASPAR_excel.xlsx',sheet_name='CASPAR',skiprows=1)
CASPAR.drop(index=0,inplace=True)
CASPAR.reset_index(drop=True,inplace=True)

#Update ages using AgeSheet
for ind in CASPAR.index:
  mem_prob = CASPAR.loc[ind,'Banyan Association Probability']
  if mem_prob == np.nan: #only update ages for objects with membership probabilities
    continue
  if mem_prob >= 0.5: #membership probability must be >50%
    SFR = CASPAR.loc[ind,'Banyan Association']
    if 'FIELD' not in SFR: #only update objects that aren't field stars
      age = AgeSheet.loc[AgeSheet['Association'] == SFR,'Age'].values[0]
      CASPAR.loc[ind,'Association Age'] = age


CASPAR.to_excel('/content/drive/MyDrive/CASPAR/Summer 2021 Work/BANYAN∑/Output.xlsx')