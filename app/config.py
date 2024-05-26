import os
import json
import sys

config_settings = json.load(open('app/config_setting.json'))

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    db_prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    db_prefix = 'sqlite:////'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = db_prefix + config_settings['database_path']
    SQLALCHEMY_TRACK_MODIFICATIONS = False