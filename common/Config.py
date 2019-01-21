import time
import platform
import configparser


class ConfigReader(object):

    def __init__(self):
        pass

    def get_config(self, config_suite, config):
        cf = configparser.ConfigParser()
        if 'Windows' in platform.platform() and 'Linux' not in platform.platform():
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Using C:/Users/sunhaoran/Documents/GitHub/Flask/flask.config ...')
            cf.read('C:/Users/sunhaoran/Documents/GitHub/Flask/flask.config')
        elif 'Linux' in platform.platform() and 'Ubuntu' not in platform.platform():
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Using /home/pi/Documents/Github/Flask/flask.config ...')
            cf.read('/home/pi/Documents/Github/Flask/flask.config')
        elif 'Ubuntu' in platform.platform():
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Using /root/Documents/GitHub/Flask/flask.config ...')
            cf.read('/root/Documents/GitHub/Flask/flask.config')
        return cf.get(config_suite, config)
