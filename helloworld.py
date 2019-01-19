import os
import time
import datetime
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory

app = Flask(__name__)


@app.route('/')
def index():
    spring = datetime.datetime(2019, 2, 5, 0, 0, 0)
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    today = datetime.datetime.now()
    day = (spring - today).days
    second = (spring - today).seconds
    count_seconds = second % 60
    count_minutes = second // 60 % 60
    count_hours = second // 60 // 60
    if count_hours > 24:
        count_hours = count_hours - 24
    templateData = {'time': current_time, 'count_days': day, 'count_hours': count_hours, 'count_minutes': count_minutes, 'count_seconds': count_seconds}
    return render_template('demo.html', **templateData)


@app.route('/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
