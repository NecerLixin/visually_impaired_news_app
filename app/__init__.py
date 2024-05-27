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


def create_app(browser,loop):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    if not os.path.exists(config_settings['database_path']):
        with app.app_context():
    # 检查表是否存在，如果不存在则创建
            db.create_all()
    from app.models import dbmodel
    from app.api import endpoints
    app.register_blueprint(endpoints.create_blueprint(browser,loop))

    return app