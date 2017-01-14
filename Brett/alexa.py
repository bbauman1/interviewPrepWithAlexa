import json
from random import randint
from pprint import pprint

def read_json():
	dic = {}
	with open('companies.json', 'r') as fp:
		dic = json.load(fp)
	return dic

questions = read_json()
diff = 'easy'
index = 0
indecies = []
for question in questions:
	if question['difficulty'].lower() == diff:
		indecies.append(index)
	index += 1

num = randint(0, len(indecies) - 1)

q = questions[indecies[num]]
pprint(q)