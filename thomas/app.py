import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

import pyaudio
import wave

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def startTimer(time):	
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = time
	WAVE_OUTPUT_FILENAME = "interViewRecording.wav"

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
	print Diff
	print type(Diff)
	if not isinstance(Diff, basestring) or Diff.lower().strip() not in ['easy', 'medium', 'hard']:
		return question(render_template('invalid_question_difficulty')).reprompt('Would you liked an easy, medium, or hard problem')

	norm_difficulty = Diff.lower().strip()
	print norm_difficulty
	if norm_difficulty == 'easy':
		startTimer(20);
		return statement('Easy question')
	elif norm_difficulty == 'medium':
		return statement('Medium question')
	return statement('Hard question')

@ask.intent('AMAZON.HelpIntent')
def help_intent():
	message = "Ask again"
	return question(message).reprompt(message)


if __name__ == '__main__':
    app.run(debug=True)


