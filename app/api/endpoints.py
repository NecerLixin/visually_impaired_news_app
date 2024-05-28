from flask import Blueprint, jsonify, make_response, request
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
    
    
    @bp.route('/api/register',methods=['POST'])
    def register():
        account = request.form.get('account')
        password = request.form.get('password')
        vertify = request.form.get('vertify')
        date = datetime.date.today()
    
        if account and password and vertify is not None:
            # 检查是否存在用户
            user_check = User.query.filter_by(user_account=account).count()
            if user_check > 0:
                print("用户已存在")
                resp = make_response(jsonify(msg="账号已存在"))
                resp.status_code = 403
                return resp
            else:
                user = User(user_account=account,
                            user_password=password,
                            create_time=date
                            )
                db.session.add(user)
                db.session.commit()
                print("注册成功")
                resp = make_response(jsonify(msg="注册成功"))
                resp.status_code = 200
                return resp
        else:
            resp = make_response(jsonify(msg="格式错误"))
            resp.status_code = 400
            return resp
        
    
    return bp


