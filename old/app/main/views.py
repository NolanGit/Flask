import re
import time
import datetime

from flask import render_template, session, redirect, url_for, current_app, flash, request
from .. import db
from ..models import User, System, SysDate
from ..email import send_email
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    ip = request.remote_addr
    from geolite2 import geolite2
    reader = geolite2.reader()
    if (str(ip) !='127.0.0.1')and ('192.168'not in str(ip)) and ('China' not in str(reader.get(ip)))and ('Beijing' not in str(reader.get(ip))):
        geolite2.close()
        return  render_template('403.html', ip=ip)
    else:
        geolite2.close()
        name = session.get('name')
        if name:
            name=name[:1]
        return render_template('index.html', name=name)


@main.route('/readme')
def readme():
    return render_template('readme.html')
