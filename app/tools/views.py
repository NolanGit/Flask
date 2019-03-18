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
    gold_price=GoldPrice.select().where(GoldPrice.crawling_times==0)
    for price in gold_price:
        datas['data'].append({'date':str(price.date),'price':price.price})
    print(datas)
    content = json.dumps(datas)
    resp = Response_headers(content)
    return (resp)

@tools.route('/app', methods=['GET', 'POST'])
def app():
    return render_template('tools/app.html')

@tools.route('/appDetail', methods=['GET'])
def appDetail():
    datas = {"data":[]}
    app_price=AppPrice.select().limit(1).order_by(-AppPrice.id).where(AppPrice.date==datetime.datetime.now().date())
    for price in app_price:
        today_crawling_time=price.crawling_times
    app_price=AppPrice.select().order_by(AppPrice.id).where((AppPrice.date==datetime.datetime.now().date())&(AppPrice.crawling_times==today_crawling_time))
    for price in app_price:
        datas['data'].append({'name':str(price.app_name),'price':price.price})
    print(datas)
    content = json.dumps(datas)
    resp = Response_headers(content)
    return (resp)
    
