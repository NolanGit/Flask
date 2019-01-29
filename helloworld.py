import os
import time
import datetime
from flask import Flask
from flask import request, redirect, url_for, session, flash
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask import render_template
from flask import send_from_directory
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'hard to guess string'

global name


class NameForm(FlaskForm):
    name = StringField('请输入您的名字，查看春节倒计时：', validators=[DataRequired()])
    submit = SubmitField('提交')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    global name
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('您似乎更改了名字！')
        session['name'] = form.name.data
        return redirect(url_for('new_year'))
    return render_template('index.html', form=form, name=session.get('name'))
    

@app.route('/new_year')
def new_year():
    global name
    spring_festival = datetime.datetime(2019, 2, 5, 0, 0, 0)
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    today = datetime.datetime.now()
    day = (spring_festival - today).days
    second = (spring_festival - today).seconds
    count_seconds = second % 60
    count_minutes = second // 60 % 60
    count_hours = second // 60 // 60
    current_utctime = datetime.datetime.utcnow()
    if count_hours > 24:
        count_hours = count_hours - 24
    templateData = {
        'name': session.get('name'),
        'time': current_time,
        'count_days': day,
        'count_hours': count_hours,
        'count_minutes': count_minutes,
        'count_seconds': count_seconds,
        'current_utctime': current_utctime
    }
    return render_template('new_year.html', **templateData)


@app.route('/tools')
def tools():
    #flash('Loading...')
    for x in range(100):
        current_ip = os.popen("curl icanhazip.com").read()
        current_ip = str(current_ip.replace("\n", ""))
        if current_ip != None and current_ip != '':
            break
        else:
            print("WARNING: Current extranet IP is : " + current_ip)
            raise Exception("Bad requests !")
    print("Current extranet IP is : " + current_ip)
    templateData = {'ip': current_ip}
    return render_template('tools.html', **templateData)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
