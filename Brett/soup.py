import requests
from bs4 import BeautifulSoup
import re

html = requests.get("https://leetcode.com/problems/two-sum/")

soup = BeautifulSoup(html.text, "lxml")

companies = soup.find(id="tags")

spans = soup.find_all("span", class_="hidebutton")
for span in spans:
	
	print span.text



