from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
import asyncio
from pyppeteer import launch
import os
import json

config_settings = json.load(open('app/config_setting.json'))




db = SQLAlchemy()
migrate = Migrate()

async def init_browser():
    print("浏览器初始化")
    return await launch(headless=True,autoClose=False)

async def init_browser():
    print("浏览器初始化")
    return await launch(headless=True,autoClose=False)

async def keep_browser_running():
    global browser
    browser = await init_browser()
    while True:
        await asyncio.sleep(100) 
    # while True:

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
browser = loop.run_until_complete(init_browser())  


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    # if not os.path.exists(config_settings['database_path']):
    #     with app.app_context():
    # # 检查表是否存在，如果不存在则创建
    #         db.create_all()
    if config_settings['database_tables_exist'] == False:
        with app.app_context():
            db.create_all()
        config_settings['database_tables_exist'] = True
        with open('app/config_setting.json') as f:
            json.dump(config_settings,f)
    from app.models import dbmodel
    from app.api import endpoints
    app.register_blueprint(endpoints.create_blueprint(browser,loop))

    return app