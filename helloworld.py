import os
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('demo.html')

@app.route('/favicon.ico')
def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000) 
