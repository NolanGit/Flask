import os
import time
import datetime
from flask import Flask
from flask import request
from flask_moment import Moment
from flask import render_template
from flask import send_from_directory
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    spring_festival = datetime.datetime(2019, 2, 5, 0, 0, 0)
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    today = datetime.datetime.now()
    day = (spring_festival - today).days
    second = (spring_festival - today).seconds
    count_seconds = second % 60
    count_minutes = second // 60 % 60
    count_hours = second // 60 // 60
    if count_hours > 24:
        count_hours = count_hours - 24
    templateData = {'time': current_time, 'count_days': day, 'count_hours': count_hours, 'count_minutes': count_minutes, 'count_seconds': count_seconds}
    return render_template('demo.html', **templateData)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
