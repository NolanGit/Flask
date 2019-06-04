import re
import time
import requests
import datetime

from flask import render_template, session, redirect, url_for, current_app, request,jsonify
from . import main
from flask_cors import cross_origin

@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def catch_all(path):
    response={}
    location="beijing"
    key='9c682a98909146c7910657e21aa9dad1'
    url='https://free-api.heweather.net/s6/weather'
    
    payload = {'location': location, 'key': key}
    r=requests.post(url, params=payload)

    response['fl']=r.json()['HeWeather6'][0]['now']['fl']
    response['tmp']=r.json()['HeWeather6'][0]['now']['tmp']
    response['wind']=r.json()['HeWeather6'][0]['now']['wind_dir']+str(r.json()['HeWeather6'][0]['now']['wind_sc'])+'级'
    response['cond_code_d']=r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_code_d']
    response['cond_txt_d']=r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_txt_d']
    response['cond_code_n']=r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_code_n']
    response['cond_txt_n']=r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_txt_n']
    response['tmp_max']=r.json()['HeWeather6'][0]['daily_forecast'][0]['tmp_max']
    response['tmp_min']=r.json()['HeWeather6'][0]['daily_forecast'][0]['tmp_min']
    response['tomorrow_cond_code_d']=r.json()['HeWeather6'][0]['daily_forecast'][1]['cond_code_d']
    response['tomorrow_cond_txt_d']=r.json()['HeWeather6'][0]['daily_forecast'][1]['cond_txt_d']
    response['tomorrow_tmp_max']=r.json()['HeWeather6'][0]['daily_forecast'][1]['tmp_max']
    response['tomorrow_tmp_min']=r.json()['HeWeather6'][0]['daily_forecast'][1]['tmp_min']
    r = requests.get('https://free-api.heweather.net/s6/air/now', params=payload)
    response['aqi']=r.json()['HeWeather6'][0]['air_now_city']['aqi']
    return jsonify(response)
