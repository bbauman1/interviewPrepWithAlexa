import logging
import json
import pyrebase

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

def start_time(minutes, questionTitle):
	seconds = minutes*60
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = seconds
	WAVE_OUTPUT_FILENAME = questionTitle+".wav"
	
	p = pyaudio.PyAudio()
	
	stream = p.open(format=FORMAT,
	                channels=CHANNELS,
	                rate=RATE,
	                input=True,
	                frames_per_buffer=CHUNK)
	
	print("* recording")
	
	frames = []
	
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)
	
	print("* done recording")
	
	stream.stop_stream()
	stream.close()
	p.terminate()
	
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()


	config = {
  		"apiKey": "AIzaSyBLJ0riHM8Z-GumKhRDOUFofYPel4AhJmU",
  		"authDomain": "alexa-76077.firebaseapp.com",
  		"databaseURL": "https://alexa-76077.firebaseio.com",
  		"storageBucket": "alexa-76077.appspot.com"
	}

	firebase = pyrebase.initialize_app(config)


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
	start_timer(20)

	return question(q['description'] + 'Would you like me to repeat the question?')

@ask.intent('QuestionExample')
def example_for_question():
	if 'company' not in session.attributes:
		return question('Question not found please ask for another')
	q = session.attributes['company']

	if 'example' not in q:
		return question('No example available. Would you like me to repeat the question?')
	
	return question(q['example']+'. Would you like to repeat the example or question?')

@ask.intent('YesRepeat')
def repeat_question():
	return question(session.attributes['company']['description'] + 'Would you like me to repeat the question or give a an example?')

@ask.intent('NoRepeat')
def repeat_question():
	return statement('Good luck! When you are done plug in your answer into leetcode! papa bless')

@ask.intent('AMAZON.HelpIntent')
def help_intent():
	message = "Ask again"
	return question(message).reprompt(message)


if __name__ == '__main__':
    app.run(debug=True)


