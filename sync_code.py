# coding=utf-8
import os
from common.Config import ConfigReader

config_reader = ConfigReader()
JENKINS_WORKSPACE = config_reader.get_config('config', 'JENKINS_WORKSPACE')
APP_LOCATION = config_reader.get_config('config', 'APP_LOCATION')

os.popen('rm -rf %s' % APP_LOCATION)
os.popen('cp -R %s' % JENKINS_WORKSPACE + '/. ' + APP_LOCATION)
