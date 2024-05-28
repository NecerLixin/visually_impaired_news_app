from flask import Blueprint, jsonify, make_response, request
from app.crawlers.scrapy3 import news_storage
from app.models.dbmodel import *
import datetime
def create_blueprint_crawl(browser=None,loop=None):
    bp = Blueprint('crawl', __name__)
        
    @bp.route('/crawl', methods=['GET'])
    def crawl():
        day_del = int(request.args.get("daydel"))
        resp = make_response()
        if day_del is not None:
            date = datetime.date.today() - datetime.timedelta(days=day_del)
            news_storage(browser,loop,date=date,store_as_json='news527.json')
            resp.set_data(jsonify(msg='爬虫完成'))
            resp.status_code = 200
        else:
            resp.set_data(jsonify(msg='请求格式错误'))
            resp.status_code = 400
        return resp
    return bp
        


def create_blueprint_news():
    bp = Blueprint('news',__name__)
    @bp.route('/news/getnews',methods=['GET'])
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
    
    # @bp.route('/news/newscontent',methods=['GET'])
    # def getnews_content():
        
    return bp

def create_blueprint_users():
    bp = Blueprint('users',__name__)
    @bp.route('/users/register',methods=['POST'])
    def register():
        account = request.form.get('account')
        password = request.form.get('password')
        verify = request.form.get('vertify')
        date = datetime.date.today()
        resp = make_response()
        if account and password and verify is not None:
            # 检查是否存在用户
            user_check = User.query.filter_by(user_account=account).count()
            if user_check > 0:
                print("用户已存在")
                resp.set_data(jsonify(msg="账号已存在"))
                resp.status_code = 403
                # 服务器理解客户端请求，但是拒绝执行此次请求
                return resp
            else:
                user = User(user_account=account,
                            user_password=password,
                            create_time=date
                            )
                db.session.add(user)
                db.session.commit()
                print("注册成功")
                resp.set_data(jsonify(msg="注册成功"))
                resp.status_code = 200
                # 请求成功
                return resp
        else:
            resp.set_data(jsonify(msg="格式错误"))
            resp.status_code = 400
            # 400 表示请求语法错误，服务器无法理解
            return resp
    
    @bp.route('/users/login',methods=['POST'])
    def login():
        """
        登陆api，POST请求传输内容： \n
        {
            "account": 用户账号,
            "password":用户密码
        }

        Returns:
            _type_: _description_
        """
        account = request.form.get('account')
        password = request.form.get('password')
        resp = make_response()
        
        if account and password is not None:
            user = User.query.filter_by(user_account=account).first()
            if user:
                user_password = user.user_password
                if password == user_password:
                    resp.set_data(jsonify(msg='登陆成功'))
                    resp.status_code = 200
                    return resp
                else:
                    resp.set_data(jsonify(mgs="账号错误"))
                    resp.status_code = 403
                    # 理解客户段请求，但是拒绝
                    return resp

            else :
                resp = make_response(jsonify(msg="用户不存在"))
                resp.status_code = 406
                # 服务器无法根据客户端请求的内容特性完成请求
                return resp
        
    
    return bp


