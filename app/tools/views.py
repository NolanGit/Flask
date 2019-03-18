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

@tools.route('/goldDetail')
def goldDetail():
    datas = {"data":[]}
    gold_price=GoldPrice.select().where('crawling_times'==1)
    for price in gold_price:
        datas['data'].append({'date':price.date,'price':price.price})
    print(datas)
    datas = {
		"data":[
			{"name":"allpe","num":100},
			{"name":"peach","num":123},
			{"name":"Pear","num":234},
			{"name":"avocado","num":20},
			{"name":"cantaloupe","num":1},
			{"name":"Banana","num":77},
			{"name":"Grape","num":43},
			{"name":"apricot","num":0}
		]
	}
    content = json.dumps(datas)
    resp = Response_headers(content)
    return (resp)
