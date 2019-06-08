import pandas as pd
import re
import operator
import numpy as np

df = pd.read_csv('a2_cleanData.csv')

number_of_recepies = len(pd.unique(df['name']))
all_ing_counts = {}

df['newaddedcolumn'] = df['ingredient'].str.split()

df = df.groupby(['url', 'name'])['newaddedcolumn'].agg(sum).reset_index()

for i in range(0,len(df)):
	itemSet = set(df['newaddedcolumn'][i])
	for item in itemSet:
		all_ing_counts[item] = all_ing_counts.get(item,0)+1

removeWords = ['cup','packed','spoon','ounce','pound','all','purpose','unsalted','baking','or','large','extract','pure','granulated','brown']
list_keys = list(all_ing_counts.keys())
for k in list_keys:
	if any(word in k for word in removeWords):
		all_ing_counts.pop(k)

sorted_d = dict(sorted(all_ing_counts.items(), key=operator.itemgetter(1),reverse =True))

finalDf = pd.DataFrame({'ingredient' : list(sorted_d.keys())[:10], 'count' : list(sorted_d.values())[:10]})

finalDf['proportion'] = finalDf['count'] / number_of_recepies

finalDf.to_csv('a2_results.csv',index = False)
