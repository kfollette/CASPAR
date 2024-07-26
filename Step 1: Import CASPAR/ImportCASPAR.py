import pandas as pd
import numpy as np

from google.colab import auth
auth.authenticate_user()
import gspread
from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)

wb = gc.open_by_url('https://docs.google.com/spreadsheets/d/1QbJHcrndhaP2JIrBazy4zcUULpgClCdt76nMilKfRNs/edit?gid=871681305#gid=871681305')
sheet = wb.worksheet('CASPAR')

data = sheet.get_all_values()

CASPAR = pd.DataFrame(data)
CASPAR.drop(1, inplace=True)
CASPAR.reset_index()
CASPAR.columns = CASPAR.iloc[0]
CASPAR = CASPAR.iloc[1:]
CASPAR = CASPAR.reset_index().drop(columns='index')