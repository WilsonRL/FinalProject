# Import libraries
import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from gtts import gTTS

NUMBER_OF_BUTTONS = 12
UPLOAD_FOLDER = '/home/pi/Desktop/serverFiles'
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def setBoard():
    return render_template("form.html")

# note: it's the string in the [] that needs to be the same as the name string in the html file
@app.route('/', methods = ['POST'])
def setBoard_Post():
    file = open("words.txt", "w")
    file.close()
    for i in range(NUMBER_OF_BUTTONS):
        word = request.form['button{}'.format(i)]
        file = open("words.txt", "a")
        file.write("{}\n".format(word))
        soundFile = gTTS(text = word, lang = 'en', slow = False)
        soundFile.save("{}.mp3".format(i))
    file.close()
    return "Your board has been reset"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
