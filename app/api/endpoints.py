from flask import Blueprint, jsonify
from app.crawlers.scrapy3 import news_storage

def create_blueprint(browser=None,loop=None):
    bp = Blueprint('api', __name__)
        
    @bp.route('/crawl', methods=['GET'])
    def crawl():
        news_storage(browser,loop,store_as_json='news527.json')
        return "yes"

    return bp

