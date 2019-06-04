import re
import json
import time
import peewee
import random
import requests
import platform
import datetime
import configparser

from flask import render_template, session, redirect, url_for, current_app, flash, Response, request
from .. import db
from ..models import User, System, SysDate
from ..data_models import App, AppPrice, GoldPrice
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
    datas = {'data': []}
    gold_price = GoldPrice.select().where(GoldPrice.crawling_times == 0)
    for price in gold_price:
        datas['data'].append({'date': str(price.date), 'price': price.price})
    content = json.dumps(datas)
    resp = Response_headers(content)
    return (resp)


@tools.route('/app', methods=['GET', 'POST'])
def app():
    return render_template('tools/app.html')


@tools.route('/appDetail', methods=['GET'])
def appDetail():
    datas = {'data': []}
    app_price = AppPrice.select().limit(1).order_by(-AppPrice.id).where(AppPrice.date == datetime.datetime.now().date())
    for price in app_price:
        today_crawling_time = price.crawling_times
        price_time = price.time
        price_date = price.date
    datas['price_time'] = str(price_time)
    datas['price_date'] = str(price_date)
    app_price = AppPrice.select().order_by(AppPrice.id).where((AppPrice.date == datetime.datetime.now().date()) & (AppPrice.crawling_times == today_crawling_time))
    for price in app_price:
        datas['data'].append({'name': str(price.app_name), 'price': price.price})
    content = json.dumps(datas)
    resp = Response_headers(content)
    return (resp)


@tools.route('/appCounts', methods=['GET'])
def appCounts():
    datas = {'data': []}
    app_query = App.select()
    for app in app_query:
        datas['data'].append({'id': str(app.id), 'app_name': str(app.app_name), 'expect_price': app.expect_price})
    content = json.dumps(datas)
    resp = Response_headers(content)
    return (resp)


@tools.route('/appDelete', methods=['POST'])
def appDelete():
    pass


@tools.route('/appEdit', methods=['POST'])
def appEdit():
    app_name, expect_price = request.form['app_name'], request.form.get('expect_price')
    pass


@tools.route('/weather', methods=['GET', 'POST'])
def weather():
    return render_template('tools/weather.html')


@tools.route('/weatherNow', methods=['GET', 'POST'])
def weatherNow():
    datas = {'data': []}
    cf = configparser.ConfigParser()
    if 'Windows' in platform.platform() and 'Linux' not in platform.platform():
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Using C:/Users/sunhaoran/Documents/GitHub/ServerTools/ServerTools.config ...')
        cf.read('C:/Users/sunhaoran/Documents/GitHub/ServerTools/ServerTools.config')
    elif 'Linux' in platform.platform() and 'Ubuntu' not in platform.platform():
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Using /home/pi/Documents/Github/ServerTools/RaspberryPi.config ...')
        cf.read('/home/pi/Documents/Github/RaspberryPi.config')
    elif 'Ubuntu' in platform.platform():
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Using /root/Documents/GitHub/ServerTools/ServerTools.config ...')
        cf.read('/root/Documents/GitHub/ServerTools/ServerTools.config')
    key = (cf.get('config', 'KEY'))
    payload = {'location': 'changchun', 'key': key}
    r = requests.get('https://free-api.heweather.net/s6/weather', params=payload)
    datas['data'].append({
        'today_forecast_cond_txt_d': r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_txt_d'],  #今日白天天气状况
        'today_forecast_cond_txt_n': r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_txt_n'],  #今日夜天天气状况
        'today_forecast_pop': r.json()['HeWeather6'][0]['daily_forecast'][0]['pop'],  #今日降水概率
        'today_forecast_tmp_max': r.json()['HeWeather6'][0]['daily_forecast'][0]['tmp_max'],  #今日最高温度
        'today_forecast_tmp_min': r.json()['HeWeather6'][0]['daily_forecast'][0]['tmp_min'],  #今日最低温度
        'today_forecast_wind_sc': r.json()['HeWeather6'][0]['daily_forecast'][0]['wind_sc'],  #今日风力状况
        'now_cond_txt': r.json()['HeWeather6'][0]['now']['cond_txt'],  #当前天气状况
        'now_tmp': r.json()['HeWeather6'][0]['now']['tmp'],  #当前气温
        'now_fl': r.json()['HeWeather6'][0]['now']['fl'],  #当前体感温度
        'now_wind_sc': r.json()['HeWeather6'][0]['now']['wind_sc'],  #当前风力
        'lifestyle_confort': r.json()['HeWeather6'][0]['lifestyle'][0]['brf'],  #舒适指数概述
        'lifestyle_confort_detail': r.json()['HeWeather6'][0]['lifestyle'][0]['txt'],  #舒适指数详情
        'lifestyle_clothes': r.json()['HeWeather6'][0]['lifestyle'][1]['brf'],  #穿衣指数概述
        'lifestyle_clothes_detail': r.json()['HeWeather6'][0]['lifestyle'][1]['txt'],  #穿衣指数详情
        'lifestyle_cold': r.json()['HeWeather6'][0]['lifestyle'][2]['brf'],  #感冒指数概述
        'lifestyle_cold_detail': r.json()['HeWeather6'][0]['lifestyle'][2]['txt'],  #感冒指数详情
        'lifestyle_working': r.json()['HeWeather6'][0]['lifestyle'][3]['brf'],  #健身指数概述
        'lifestyle_working_detail': r.json()['HeWeather6'][0]['lifestyle'][3]['txt'],  #健身指数详情
        'lifestyle_makeup': r.json()['HeWeather6'][0]['lifestyle'][-3]['brf'],  #化妆指数概述
        'lifestyle_makeup_detail': r.json()['HeWeather6'][0]['lifestyle'][-3]['txt'],  #化妆指数详情
        'lifestyle_air': r.json()['HeWeather6'][0]['lifestyle'][-1]['brf'],  #空气指数概述
        'lifestyle_air_detail': r.json()['HeWeather6'][0]['lifestyle'][-1]['txt'],  #空气指数详情
        'time': r.json()['HeWeather6'][0]['update']['loc']
    })
    content = json.dumps(datas)
    resp = Response_headers(content)
    return (resp)


@tools.route('/weatherTrend', methods=['GET', 'POST'])
def weatherTrend():
    datas = {'data': []}
    app_query = App.select()
    for app in app_query:
        datas['data'].append({'id': str(app.id), 'app_name': str(app.app_name), 'expect_price': app.expect_price})
    content = json.dumps(datas)
    resp = Response_headers(content)
    return (resp)