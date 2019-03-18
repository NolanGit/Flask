import re
import json
import time
import peewee
import random
import datetime

from flask import render_template, session, redirect, url_for, current_app, flash,Response
from .. import db
from ..models import User, System, SysDate
from ..data_models import AppPrice,GoldPrice
from ..email import send_email
from . import tools


def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@tools.route('/gold', methods=['GET', 'POST'])
def gold():
    return render_template('tools/gold.html')

@tools.route('/goldDetail', methods=['GET'])
def goldDetail():
    datas = {"data":[]}
    gold_price=GoldPrice.select().where(GoldPrice.crawling_times==1)
    for price in gold_price:
        datas['data'].append({'date':price.date,'price':price.price})
    print(datas)
    content = json.dumps(datas)
    resp = Response_headers(content)
    return (resp)
