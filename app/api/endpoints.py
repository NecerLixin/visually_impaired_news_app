from flask import Blueprint, jsonify,make_response
from app.crawlers.scrapy3 import news_storage
from app.models.dbmodel import *
import datetime
def create_blueprint(browser=None,loop=None):
    bp = Blueprint('api', __name__)
        
    @bp.route('/crawl', methods=['GET'])
    def crawl():
        news_storage(browser,loop,store_as_json='news527.json')
        return "yes"
    
    @bp.route('/api/getnews',methods=['GET'])
    def getnews():
        date = datetime.date.today()
        date_str = date.strftime("%y%m%d")
        news_list = News.query.filter_by(news_date=date_str).all()
        news_data = []
        for news in news_list:
            news_dict = {
                'news_id': news.news_id,
                'news_category': news.news_category,
                'news_time': news.news_time,
                'new_img_url': news.new_img_url,
                'page_url': news.page_url,
                'source': news.source,
                'tag': news.tag,
                'news_title': news.news_title,
                'news_author': news.news_author,
                'news_date': news.news_date,
            }
            news_data.append(news_dict)
        data = str(news_data)
        response = make_response(data)
        response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        return response
        
    return bp


