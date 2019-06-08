import pandas as pd
import re
import unicodedata
import numpy as np

df = pd.read_csv('a2_rawData.csv')

df['ingredient'] = df['ingredient'].str.normalize('NFC').str.encode('ascii', 'ignore').str.decode('utf-8')
df['ingredient'] = df['ingredient'].str.split(',').str[0]
df['ingredient'] = df['ingredient'].str.replace('-', ' ').str.replace(r'[\d / . * ()]', ' ').str.strip().str.lower()
df['ingredient'] = df['ingredient'].str.replace(r' +', ' ')

df['ingredient'].replace('', np.NaN, inplace = True)
df = df.dropna()

df.to_csv('a2_cleanData.csv',index = False)