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
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent('Default')
def default_quesiton():
	return question('come again hombre...?')

@ask.intent('GetQuestion')
def get_question():
	return statement('No questions yet fuck off dude')

@ask.intent('NoobQuestion')
def noob_question():
	message = "For zero to one hundred, print fizz if the number is even, and print buzz if the number is odd"
	return statement(message)

@ask.intent('QuestionByDifficulty', convert={'Diff':'string'})
def question_type_difficulty(Diff):
	if not isinstance(Diff, basestring) or Diff.lower().strip() not in ['easy', 'medium', 'hard']:
		return question(render_template('invalid_question_difficulty')).reprompt('Would you liked an easy, medium, or hard problem')

	norm_difficulty = Diff.lower().strip()
	q = get_difficulty(norm_difficulty)

	session['company'] = q 

	return statement(q['description'])

@ask.intent('AMAZON.HelpIntent')
def help_intent():
	message = "Ask again"
	return question(message).reprompt(message)


if __name__ == '__main__':
    app.run(debug=True)


