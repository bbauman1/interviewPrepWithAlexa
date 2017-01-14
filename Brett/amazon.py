import requests
from bs4 import BeautifulSoup
import re
import json
import os
import urllib2



url = os.getcwd() + "/amazon-qs.htm"
page = open(url)
soup = BeautifulSoup(page.read(), "lxml")
links = []

problems = soup.findAll(href=re.compile('.*problem.*'))
for p in problems:
	links.append(p['href'])


