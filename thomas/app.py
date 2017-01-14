import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def welcome_intern():
    welcome_msg = render_template('welcome')
    return statement(welcome_msg)

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

@ask.intent('AMAZON.HelpIntent')
def help_intent():
	message = "Ask again"
	return question(message).reprompt(message)


if __name__ == '__main__':
    app.run(debug=True)
