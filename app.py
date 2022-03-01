#REFERENCES
# https://projects.raspberrypi.org/en/projects/python-web-server-with-flask
# https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/

import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/pi/Desktop/webapp'
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check that its the correct file type
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name = filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
    <input type=file name=file>
    <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

##@app.route('/')
##def index():
##    return render_template('index.html')
##
##@app.route('/cakes')
##def cakes():
##    return render_template('cakes.html')
##    # return 'Yummy cakes!'
##
##@app.route('/hello/<name>')
##def hello(name):
##    return render_template('page.html', name=name)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
