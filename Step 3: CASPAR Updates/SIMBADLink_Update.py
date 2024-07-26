import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

from google.colab import drive
drive.mount('/content/drive')
df = pd.read_csv('/content/drive/MyDrive/Code/Code_Files/caspar_new.csv')
#Below gets rid of units column, for doing comparisons and searches to avoid errors
df.reset_index(drop=True,inplace=True)

#store front and back half of html link
link = ["https://simbad.u-strasbg.fr/simbad/sim-id?Ident=","&submit=submit+id"]

#store special characters and their rules in dictionary
rules = {'[':'%5B',']':'%5D','+':'%2B',' ':'+'}
char_list = ['[',']','+',' ']

#Add new column for links
df['Links'] = ''

for ind in df.index:
  #grab simbad name
  string = df.loc[ind,'Simbad-Resolvable Name']
  #empty string to rewrite name with html rules applied
  html_name = ''
  for c in string:
    if c in char_list:
      html_name += rules[c]
    else:
      html_name += c
  #append full link with all pieces
  df.loc[ind,'Links'] = link[0] + html_name + link[1]

  df.to_excel('/content/drive/MyDrive/Code/Code_Files/caspar_links.xlsx')