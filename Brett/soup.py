# from urllib.request import urlopen
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import re

# html = requests.get("https://leetcode.com/problems/linked-list-cycle/")
html = requests.get('https://leetcode.com/accounts/login/', auth=('bbauman1', 'Judgedr3dd'))
print(html.text)
# soup = BeautifulSoup(html.text, "lxml")
# print(soup.prettify())
# companies = soup.find(id="company_tags")
# print companies


import requests

# Fill in your details here to be posted to the login form.
payload = {
    'inUserName': 'bbauman1',
    'inUserPass': 'Judgedr3dd'
}

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    p = s.post('LOGIN_URL', data=payload)
    # print the html returned or something more intelligent to see if it's a successful login page.
    print p.text

    # An authorised request.
    r = s.get('A protected web page url')
    print r.text
        # etc...