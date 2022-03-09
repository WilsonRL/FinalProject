# [1] https://projects.raspberrypi.org/en/projects/python-web-server-with-flask/2
# [2] https://www.geeksforgeeks.org/retrieving-html-from-data-using-flask/
# [3] https://www.codegrepper.com/code-examples/python/input+box+for+text+in+flask
# [4] https://www.w3schools.com/python/python_file_write.asp
# [5] https://www.w3schools.com/python/python_file_open.asp


from flask import Flask, render_template, request
from gtts import gTTS

NUMBER_OF_BUTTONS = 12

app = Flask(__name__)

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
        soundFile.save("button{}.mp3".format(i))
    file.close()
    return "Your board has been reset"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 8000)
