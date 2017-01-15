import pyrebase
import pyaudio
import wave

def start_timer(minutes):
        seconds = minutes*60
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = seconds

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
	return [p, stream, frames]

def stop_timer(streamObj, questionTitle, pId, description):
	FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        WAVE_OUTPUT_FILENAME = questionTitle+".wav"
	p = streamObj[0]
	stream = streamObj[1]
	frames = streamObj[2]

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
        print "wrote file"

	config = {
                "apiKey": "AIzaSyBLJ0riHM8Z-GumKhRDOUFofYPel4AhJmU",
                "authDomain": "alexa-76077.firebaseapp.com",
                "databaseURL": "https://alexa-76077.firebaseio.com",
                "storageBucket": "alexa-76077.appspot.com",
                "serviceAccount": "alexa-9d48e19977cf.json"
        }

        firebase = pyrebase.initialize_app(config)
        print "Firebase: ", firebase

        #print "Storage obj:", storage, "Storage string", storage.__str()
        #print "Storage.child():", storage.child('audioFiles/' + WAVE_OUTPUT_FILENAME)
        storage = firebase.storage()
        storage.child(str(pId)).put(WAVE_OUTPUT_FILENAME)
        storageURL = storage.child(str(pId)).get_url('')
        print "Storage URL: ", storageURL
        db = firebase.database()
        data = {'description': description, 'name': questionTitle, 'url': storageURL}
        db.child('problems').child(pId).set(data)
        print "set it all..."

timer = start_timer(3)

usrInput = raw_input('End?')
while usrInput != 'end':	
	usrInput = raw_input('End?')
stop_timer(timer, "Title Of The Thing", 45, "Simple description jah feel?")



