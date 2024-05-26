from flask import Blueprint, jsonify
from app.crawlers.scrapy import get_news, news_storage

def create_blueprint(browser,loop):
    bp = Blueprint('api', __name__)

    @bp.route('/crawl', methods=['GET'])
    async def crawl():
        await news_storage(browser,loop, store_as_json='news_526.json')
        print('完成新闻爬取并添加到数据库')
        return jsonify({'message': 'Articles fetched and saved successfully'})

    return bp

