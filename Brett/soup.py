import requests
from bs4 import BeautifulSoup
import re
import json
import os
import urllib2
from pprint import pprint

def read_json():
	dic = {}
	with open('all.json', 'r') as fp:
		dic = json.load(fp)
	return dic

def write_json(dic):
	with open('all.json', 'w') as fp:
		json.dump(dic, fp, sort_keys=True, indent=4)

url = os.getcwd() + "/all.html"
page = open(url)
soup = BeautifulSoup(page.read(), "lxml")
links = []
count = 0
problems = soup.findAll(href=re.compile('.*problem.*'))
for p in problems:
	if p == '/problems/reverse-words-in-a-string-ii/':
		continue
	links.append(p['href'])


# dic = read_json()
json_arr = []

for link in links:
	count += 1
	prob = 'https://leetcode.com' + link
	dic = {}
	html = requests.get(prob)

	soup = BeautifulSoup(html.text, "lxml")

	companies = soup.find(id="tags")

	try:
		name = str(soup.title.string.split('|')[0]).strip()
		dic['name'] = name
	except:
		continue
	spans = soup.find_all("span", class_="hidebutton")
	if(len(spans) == 0):
		continue
	hints = str(spans[0].text).strip().split('\n')
	similars = []
	if(len(spans) > 1):		
		similars = str(spans[1].text).strip().split('\n')
	dic['hints'] = hints
	dic['similar_problems'] = similars

	dic['companies'] = 'Amazon'

	infos = soup.find_all("div", class_="question-info")
	info = str(infos[0].text).strip().split('\n')
	accepted = info[0].split(':')[1].strip()
	total = info[1].split(':')[1].strip()
	difficulty = info[2].split(':')[1].strip()
	dic['accepted'] = int(accepted)
	dic['total'] = int(total)
	dic['difficulty'] = difficulty

	number = soup.find("div", class_="question-title clearfix")
	q_num = str(number.text).split('.')[0].strip()	
	dic['number'] = int(q_num)

	description = soup.find("meta",  property="og:description")
	dic['description'] = str(description['content'].encode('utf-8')).strip()
	json_arr.append(dic)

# pprint(json_arr)
print count
write_json(json_arr)



