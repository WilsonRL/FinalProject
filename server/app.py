# NOTES
# you need to change the UPLOAD_FOLDER

# REFERENCES
# [01] https://projects.raspberrypi.org/en/projects/python-web-server-with-flask/2
# [02] https://www.geeksforgeeks.org/retrieving-html-from-data-using-flask/
# [03] https://www.codegrepper.com/code-examples/python/input+box+for+text+in+flask
# [04] https://www.w3schools.com/python/python_file_write.asp
# [05] https://www.w3schools.com/python/python_file_open.asp
# [06] https://www.geeksforgeeks.org/convert-text-speech-python/
# [07] https://ordinarycoders.com/blog/article/11-chart-js-examples#installation
# [08] https://blog.ruanbekker.com/blog/2017/12/14/graphing-pretty-charts-with-python-flask-and-chartjs/
# [09] https://sashamaps.net/docs/resources/20-colors/
# [10] https://www.chartjs.org/docs/latest/charts/bar.html
# [11] https://www.programiz.com/python-programming/methods/list/count
# [12] https://adafruit-io-python-client.readthedocs.io/en/latest/data.html
# [13] https://www.w3schools.com/css/css_align.asp
# [14] https://kanchanardj.medium.com/how-to-add-images-to-html-in-a-flask-app-4dbcc92e3aeb
# [15] https://kanchanardj.medium.com/redirecting-to-another-page-with-button-click-in-python-flask-c112a2a2304c

# Import libraries
import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, Markup
from werkzeug.utils import secure_filename
from gtts import gTTS
from Adafruit_IO import Client

# constants
NUMBER_OF_BUTTONS = 12
UPLOAD_FOLDER = '/Users/wilson/Desktop/combinedServer'
ALLOWED_EXTENSIONS = {'mp3', 'txt'}

# create Flask instance
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# import sensitive data from personal file
try:
    from personal import personalData
except ImportError:
    print("WiFi and io secrets are kept in personal.py, please add them there.")
    raise

# username and key from persona.py to login to adafruit io
aio_username = personalData["aio_username"]
aio_key = personalData["aio_key"]

# login and open adafruit io
aio = Client(aio_username, aio_key)

# get data from adafruit io feed
data = aio.data("aac-for-dogs")

# make list of adafruit io feed data
recordedData = []
for word in data:
    recordedData.append(word.value.lower().rstrip("\n"))

# make list of labels for graph based on words.txt file created when board is setup
labels = []
file = open("words.txt", 'r')
for word in file:
    labels.append(word.lower().rstrip("\n"))
file.close()

# use labels to count the number of times a word is pressed: these are the values for the graph
values = []
for word in labels:
    values.append(recordedData.count(word))

# renders main.html as the "home page" for the server website
@app.route('/main', methods =['GET', 'POST'])
def main():
    return render_template('main.html')

# renders the form.html page where the user submits words for the buttons
@app.route('/setboard')
def setBoard():
    return render_template("form.html")

# gets words from form.html and uses them to create the mp3 files and text file
@app.route('/setboard', methods = ['POST'])
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

# supposed to make it so you can upload files of the stated type, but I'm not sure this actually works
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# allows feather to download mp3 and txt files
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
set

# renders the bar_chart.html page that shows the number of button presses
@app.route('/graph')
def index():
    bar_labels=labels
    bar_values=values
    return render_template('bar_chart.html', title='Number of Button Presses', max=1000, labels=bar_labels, values=bar_values)

# runs server
if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 8000)
