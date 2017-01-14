import logging
import json

from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

with open('companies.json', 'r') as f:
	q_dict = json.load(f)

def get_difficulty(diff):
	questions = []
	for q in q_dict:
		if q['difficulty'].lower() == diff:
			questions.append(q)
	real_q = questions[randint(0, len(questions) - 1)]
	return real_q

@ask.launch
def welcome_intern():
    return question(render_template('welcome'))

@ask.intent('Default')
def default_quesiton():
	return question('come again hombre...?')

@ask.intent('QuestionByDifficulty', convert={'Diff':'string'})
def question_type_difficulty(Diff):
	if not isinstance(Diff, basestring) or Diff.lower().strip() not in ['easy', 'medium', 'hard']:
		return question(render_template('invalid_question_difficulty')).reprompt('Would you liked an easy, medium, or hard problem')

	norm_difficulty = Diff.lower().strip()
	q = get_difficulty(norm_difficulty)

	session.attributes['company'] = q 
	session.attributes['difficulty'] = norm_difficulty
	print("++++++++++++++++")
	print(q['name'])
	print("++++++++++++++++")

	return question(q['description'] + ' Would you like me to repeat the question or give an example?')

@ask.intent('QuestionExample')
def example_for_question():
	if 'company' not in session.attributes:
		return question('Question not found please ask for another')
	q = session.attributes['company']

	if 'example' not in q:
		return question('No example available. Would you like me to repeat the question?')
	
	return question(q['example']+', Would you like to repeat the example or question?')

@ask.intent('YesRepeat')
def repeat_question():
	return question(session.attributes['company']['description'] + ' Would you like me to repeat the question or give a an example?')

@ask.intent('NoRepeat')
def repeat_question():
	if 'company' not in session.attributes:
		return statement('Thanks for coding with us!')
	return statement('Good luck! When you are done plug in your answer into question number {} on leetcode! papa bless'.format(session.attributes['company']['id']))

@ask.intent('Stop')
def stop_question():
	return statement('Thanks for coding with us!')

@ask.intent('AnotherQuestion')
def ask_another_question():
	if 'company' not in session.attributes:
		return question('Question not asked yet. Do you want an easy, medium, or hard coding question?')
	if 'difficulty' not in session.attributes:
		return question('Difficulty not set. Do you want an easy, medium, or hard coding question?')
	norm_difficulty = session.attributes['difficulty']
	q = get_difficulty(norm_difficulty)
	session.attributes['company'] = q 
	return question(q['description']+' Would you like me to repeat the question or give an example?')

@ask.intent('AMAZON.HelpIntent')
def help_intent():
	message = "Ask again"
	return question(message).reprompt(message)


if __name__ == '__main__':
    app.run(debug=True)


