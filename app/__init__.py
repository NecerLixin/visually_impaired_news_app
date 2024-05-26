from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
import asyncio
from pyppeteer import launch

loop = None
# 全局浏览器实例
# init_browser()



db = SQLAlchemy()
migrate = Migrate()


def create_app(browser=None,loop=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import dbmodel
    from app.api import endpoints
    app.register_blueprint(endpoints.create_blueprint(browser,loop))

    return app