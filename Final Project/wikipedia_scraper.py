
# source: https://gist.github.com/alexanderholt/d08fef44153672807c571166b592aa4e#file-wikipedia_scrape_lists-py


import wikipedia
import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import re

html = requests.get('https://en.wikipedia.org/wiki/Lists_of_American_films')

b = BeautifulSoup(html.text, 'lxml')
links = []

for i in b.find_all(name = 'li'):
	for link in i.find_all('a', href=True):
		links.append(link['href'])
year_links = ['https://en.wikipedia.org' + i for i in links]
year_links = year_links[19:137] # determined through trial and error, hard-coding may not be the best solution, but it is one
film_titles = []
film_links = []

for decade in year_links:
	print('Collecting films from {}').format(decade)
	decadeParse = decade[-4:]
	html = requests.get(decade)
	b = BeautifulSoup(html.text, 'lxml')
	for i in b.find_all(name='table', class_='wikitable'):
		for j in i.find_all(name='tr'):
            
			for k in j.find_all(name='i'):
				for link in k.find_all('a', href=True):
					try: 
						tupTitle = (link['title'], decadeParse)
					except:
					 	tupTitle = ("NULL", "", "NULL")
					try:
						film_titles.append(tupTitle)
						film_links.append(link['href'])
					except:
						pass

print('Number of Film Links Collected: {}'.format(len(film_links)))
print('Number of Film Titles Collected: {}'.format(len(film_links)))
new_film_links = [i for i in film_links if 'redlink' not in i]
new_film_titles = [i for i in film_titles if '(page does not exist)' not in i]
print('Number of Film Links with Wikipedia Pages: {}'.format(len(new_film_links)))
print('Number of Film Titles with Wikipedia Pages: {}'.format(len(new_film_titles)))

possibles = ['Plot','Synopsis','Plot synopsis','Plot summary', 'Story','Plotline','The Beginning','Summary','Content','Premise']
possibles_edit = [i + 'Edit' for i in possibles]
all_possibles = possibles + possibles_edit

for i in range(len(new_film_titles)):
    synopsis = "NULL"
    try:
        wik = wikipedia.WikipediaPage(new_film_titles[i][0])
    except:
        wik = "NULL" # tried to get put a "continue" here but apparently I don't know how those work?
    try:
        for j in all_possibles:
            if wik.section(j) != None:
                synopsis = wik.section(j).replace('\n',' ').replace("\'","")
    except:
        pass

    if synopsis != "NULL" or "": 
        fileTitle = re.sub('[*(){}<>;:?/\"\'% ]', '', new_film_titles[i][0]) #creating filenames, but need to make sure the os doesn't get angry
        fileTitle = fileTitle.encode('ascii', 'ignore') # sometimes file names work with unicode, but why mess with it?
        f = open("./plots/" + fileTitle + ".txt", 'w')
        f.write(synopsis.encode('utf8') + "\n" + new_film_titles[i][0].encode('utf8')  + "\n" +  new_film_titles[i][1])
        f.close() # resulting files are newline seperated, plot, name, year. Apparently some issues with genre have cropped up.
    
