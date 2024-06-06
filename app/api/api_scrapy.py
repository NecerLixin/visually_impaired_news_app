from flask import Blueprint, jsonify, make_response, request
from app.crawlers.scrapy3 import news_storage
from app.models.dbmodel import *
import datetime
from .utils import StatusCode

def create_blueprint_crawl(browser=None,loop=None):
    bp = Blueprint('crawl', __name__)
        
    @bp.route('/crawl', methods=['GET'])
    def crawl():
        day_del = int(request.args.get("daydel"))
        resp = make_response()
        resp.headers['Content-Type'] = 'application/json; charset=UTF-8'
        if day_del is not None:
            date = datetime.date.today() - datetime.timedelta(days=day_del)
            news_storage(browser,loop,date=date)
            resp.set_data(jsonify(msg='爬虫完成').get_data())
            resp.status_code = StatusCode.CODE_FINISH
        else:
            resp.set_data(jsonify(msg='请求格式错误').get_data())
            resp.status_code = StatusCode.CODE_SYNTAX_ERROR
        return resp
    return bp