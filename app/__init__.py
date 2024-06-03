from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from .config import Config
import asyncio
from pyppeteer import launch
import os
import json
from app.websocket.audio import socketio
from app.routes import init_routes

config_settings = json.load(open('app/config_setting.json'))



db = SQLAlchemy()
migrate = Migrate()

async def init_browser():
    print("浏览器初始化")
    return await launch(headless=True,autoClose=False)

# async def keep_browser_running():
#     global browser
#     browser = await init_browser()
#     while True:
#         await asyncio.sleep(100) 
#     # while True:

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
browser = loop.run_until_complete(init_browser())  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'secret_key'
    # app.config['JSON_AS_ASCII'] = False
    # app.config['ensure_ascii'] = False
    app.json.ensure_ascii = False
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        db.create_all()
            
    from app.models import dbmodel
    from app.api import api_scrapy,api_users,api_news,api_serach,api_tts
    from app.routes import init_routes
    from app.websocket import audio
    
    app.register_blueprint(api_scrapy.create_blueprint_crawl(browser,loop))
    app.register_blueprint(api_news.create_blueprint_news())
    app.register_blueprint(api_users.create_blueprint_users())
    app.register_blueprint(audio.websocket_bp)
    app.register_blueprint(api_serach.create_blueprint_search())
    app.register_blueprint(api_tts.create_blueprint_ttsf())
    socketio.init_app(app,cros_allow_origin='*')
    init_routes(app)
    
    return app