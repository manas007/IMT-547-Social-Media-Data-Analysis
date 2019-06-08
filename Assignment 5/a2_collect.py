import requests
from bs4 import BeautifulSoup
import os
import csv
import io

from bs4 import NavigableString
from bs4 import Tag

baseUrl = 'https://www.mybakingaddiction.com/page/'

all_recepies = []
all_recepies_urls = []

if not os.path.isfile('rep1.html'):
    for pagenumber in range(2,35):
        r = requests.get(baseUrl + str(pagenumber))
        soup = BeautifulSoup(r.text, 'html.parser')
        recepies_on_website = soup.find('div', {'id' : 'content'}).find_all('article')
        all_recepies.append(recepies_on_website)

    f = io.open('rep1.html','w+', encoding='utf-8')
    for i in range(0 , len(all_recepies)):
        for j in range(0, len(all_recepies[i])):
            f.write(str(all_recepies[i][j])+'\n')
            all_recepies_urls.append(all_recepies[i][j].find('a' , href = True)['href'])
else:
    soup = BeautifulSoup(io.open('rep1.html','r+', encoding='utf-8'), 'html.parser')
    recepies_on_website = soup.find_all('article')
    all_recepies.append(recepies_on_website)
    for i in range(0 , len(all_recepies)):
        for j in range(0, len(all_recepies[i])):
            all_recepies_urls.append(all_recepies[i][j].find('a' , href = True)['href'])

each_url_requested = None   
all_ingredients_lst = list()
for eachURL in all_recepies_urls:
    temp_list = list()
    r = requests.get(eachURL)
    each_url_requested = BeautifulSoup(r.text, 'html.parser')

    recepie_name = each_url_requested.find('h1' , {'class' : 'post-title'})
    if recepie_name is None:
        continue
    
    recepie_name = recepie_name.text

    ingredientLists = each_url_requested.find('div' , {'class' : 'mv-create-ingredients'})
    if each_url_requested is None or ingredientLists is None:
        continue
    
    ingredientLists = ingredientLists.find_all('ul')
    for ingredientList in ingredientLists:
        for ingredient in ingredientList:
            if isinstance(ingredient, NavigableString):
                continue
            if isinstance(ingredient, Tag):
                all_ingredients_lst.append([eachURL , recepie_name, ingredient.text.strip()])

with io.open('a2_rawData.csv','a', newline='',encoding = 'utf-8') as fnew:
    wr = csv.writer(fnew)
    header = ['url', 'name', 'ingredient']
    wr.writerow(header)
    wr.writerows(all_ingredients_lst)