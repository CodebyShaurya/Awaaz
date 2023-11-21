from flask import Flask,render_template, request, redirect, jsonify
import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
import random

OPENAI_API_KEY = "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"
FS = 44100  # Sample rate#
SECONDS = 5  # Duration of recording
REMEDY = {
        'P': ['Put your lips together to make the sound. ', "Vocal cords don't vibrate for voiceless sounds."],
        'B': ['Put your lips together to make the sound. '],
        'M': ['Put your lips together to make the sound. ', 'Air flows through your nose.'],
        'W': ['Put your lips together and shape your mouth like you are saying "oo".'],
        'F': ['Place your bottom lip against your upper front teeth. ', 'Top teeth may be on your bottom lip.'],
        'V': ['Place your bottom lip against your upper front teeth. ', 'Top teeth may be on your bottom lip.'],
        'S': ['Keep your teeth close together to make the sound. ',
              'The ridge right behind your two front teeth is involved. ', 'The front of your tongue is used. ',
              "Vocal cords don't vibrate for voiceless sounds."],
        'Z': ['Keep your teeth close together to make the sound. ',
              'The ridge right behind your two front teeth is involved. ', 'The front of your tongue is used.'],
        'th': ['Place your top teeth on your bottom lip and let your tongue go between your teeth for the sound. ',
               'The front of your tongue is involved.'],
        'TH': [
            'Place your top teeth on your bottom lip and let your tongue go between your teeth for the sound (as in thin). ',
            'The front of your tongue is involved.'],
        'N': ['Air flows through your nose. ', 'The ridge right behind your two front teeth is involved. ',
              'The front of your tongue is used.'],
        'NG': ['Air flows through your nose.'],
        'SING': ['Air flows through your nose.'],
        'L': ['The ridge right behind your two front teeth is involved. ', 'The front of your tongue is used.'],
        'T': ['The ridge right behind your two front teeth is involved. ', 'The front of your tongue is used. ',
              "Vocal cords don't vibrate for voiceless sounds."],
        'D': ['The ridge right behind your two front teeth is involved. ', 'The front of your tongue is used.'],
        'CH': ['The front-roof of your mouth is the right spot for the sound.'],
        'J': ['The front-roof of your mouth is the right spot for the sound. ', 'The front of your tongue is used.'],
        'SH': ['The front-roof of your mouth is the right spot for the sound. ', 'The front of your tongue is used.'],
        'ZH': ['The front-roof of your mouth is the right spot for the sound. ', 'The front of your tongue is used.'],
        'K': ['The back-roof of your mouth is the right spot for the sound. ', 'The back of your tongue is used. ',
              "Vocal cords don't vibrate for voiceless sounds."],
        'G': ['The back-roof of your mouth is the right spot for the sound. ', 'The back of your tongue is used.'],
        'R': ['The back-roof of your mouth is the right spot for the sound. ', 'The back of your tongue is used.'],
        'Y': ['The front of your tongue is used.'],
        'CH': ['The front of your tongue is used.'],
        'H': ['Your lungs provide the airflow for every sound, especially this one.']
    }
LETTERS = ['S', 'SH', 'F', 'TH', 'L', 'R', 'B', 'V', 'P', 'F', 'D', 'T']
EXAMPLE = {
        'S': 'sunday',
        'SH': 'ship',
        'F': 'free',
        'TH': 'think',
        'L': 'love',
        'R': 'rain',
        'B': 'boat',
        'V': 'very',
        'P': 'pen',
        'F': 'free',
        'D': 'door',
        'T': 'time'
    }


app = Flask(__name__)


def check(word_given, word_recieved, check_for, incorrect):
    # print(incorrect)
    para = word_given != word_recieved
    while word_given != word_recieved:
        print('Pronounciation is not correct\n')
        if word_recieved == incorrect:
            print('Use the following instructions and then repeat :\n')
            for i in REMEDY[check_for]:
                print(i)
            print('\n')
        else:
            print('Please try again\n')
        print('Say ', word_given, ' :')
        word_recieved = input()
        word_recieved = word_recieved.upper()
        # print(word_given,word_recieve)
    print('VERY GOOD!! Correct pronounciation \n')


@app.route("/generate_word", methods=["GET", "POST"])
def generate_word():
    letter = random.choice(LETTERS)
    word_data = {
        "word": EXAMPLE[letter]
    }
    return jsonify(word_data)


@app.route('/record_audio')
def record_audio():

    myrecording = sd.rec(int(SECONDS * FS), samplerate=FS, channels=2)
    sd.wait()  # Wait until recording is finished
    write('output.wav', FS, myrecording)  # Save as WAV file
    redirect('/audio_to_text')


@app.route('/audio_to_text')
def audio_to_text():

    client = OpenAI(api_key=OPENAI_API_KEY)

    audio_file = open("output.wav", "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    print(transcript)






    # for i in letters:
    #     print('Say ', example[i[0]], ' :')
    #     word_recieved = input()
    #     check(example[i[0]].upper(), word_recieved.upper(), i[0], (i[1] + example[i[0]][len(i[0]):]).upper())
    #
    #     print('Say ', example[i[1]], ' :')
    #     word_recieved = input()
    #     check(example[i[1]].upper(), word_recieved.upper(), i[1], (i[0] + example[i[1]][len(i[1]):]).upper())


if __name__=="__main__":
    app.run(debug=True, port=5000)