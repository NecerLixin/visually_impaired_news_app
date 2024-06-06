from flask import Blueprint, jsonify, make_response, request
from app.crawlers.scrapy3 import news_storage
from app.models.dbmodel import *
import datetime
from .utils import StatusCode,get_brief

def create_blueprint_news():
    bp = Blueprint('news',__name__)
    @bp.route('/news/getnews',methods=['GET'])
    def getnews():
        date = datetime.date.today()
        date_str = date.strftime("%y%m%d")
        # news_list = News.query.filter_by(news_date=date_str).all()
        news_list = News.query.order_by(News.news_date.desc()).all()[:10]
        news_data = []
        for news in news_list:
            brief = get_brief(json.loads(news.news_content))
            news_dict = {
                'news_id': news.news_id,
                'news_category': news.news_category,
                # 'news_time': news.news_time,
                'news_img_url': news.news_img_url,
                # 'page_url': news.page_url,
                # 'source': news.source,
                'tag': news.tag,
                'news_title': news.news_title,
                # 'news_author': news.news_author,
                'news_date': news.news_date,
                'brief':brief
            }
            news_data.append(news_dict)
        # data = str(news_data)
        response = make_response()
        response.set_data(jsonify(news_data).get_data())
        response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        return response
    
    @bp.route('/news/newscontent',methods=['GET'])
    def getnews_content():
        news_id = request.args.get('newsid')
        news = News.query.filter_by(news_id=news_id).first()
        resp = make_response()
        if news:
            msg = "新闻内容请求成功"
            content = news.news_content
            resp.set_data(str({"msg":msg,"content":content}))
            resp.status_code = StatusCode.CODE_FINISH
        else:
            msg = "请求失败，新闻id错误"
            resp.set_data(str({"msg":msg}))
            resp.status_code = StatusCode.CODE_CANT_FINISH
        resp.headers['Content-Type'] = 'application/json; charset=UTF-8'
        return resp
    
    @bp.route("/news/getnewsone",methods=['GET'])
    def get_news_one():
        news_id = request.args.get('id')
        news = News.query.filter_by(news_id=news_id).first()
        news_data = {
            "title":news.news_title,
            "source":news.source,
            "content":json.loads(news.news_content),
            "author":news.news_author,
            "category":news.news_category,
            "time":news.news_time
        }
        resp = make_response(jsonify(news_data))
        resp.status_code = 200
        resp.headers['Content-Type'] = 'application/json; charset=UTF-8'
        
        return resp
    
    
    return bp