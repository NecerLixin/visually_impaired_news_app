from flask import Blueprint, jsonify, make_response, request
from app.crawlers.scrapy3 import news_storage
from app.models.dbmodel import *
import datetime

class StatusCode:
    CODE_FINISTH = 200
    CODE_SYTAX_ERROR = 400
    CODE_UNDERSTAND_REFUSE = 403
    CODE_CANT_FINISHT = 406


def get_brief(content:list,length=60)->str:
    """
    根据content构建一个新闻简

    Args:
        content (list): 新闻content列表

    Returns:
        str: 新闻简介
    """
    


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
            resp.status_code = StatusCode.CODE_FINISTH
        else:
            resp.set_data(jsonify(msg='请求格式错误').get_data())
            resp.status_code = StatusCode.CODE_SYTAX_ERROR
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
    
    @bp.route('/news/newscontent',methods=['GET'])
    def getnews_content():
        news_id = request.args.get('newsid')
        news = News.query.filter_by(news_id=news_id).first()
        resp = make_response()
        if news:
            msg = "新闻内容请求成功"
            content = news.news_content
            resp.set_data(str({"msg":msg,"content":content}))
            resp.status_code = StatusCode.CODE_FINISTH
        else:
            msg = "请求失败，新闻id错误"
            resp.set_data(str({"msg":msg}))
            resp.status_code = StatusCode.CODE_CANT_FINISHT
        resp.headers['Content-Type'] = 'application/json; charset=UTF-8'
        return resp
    
    
        
    
    
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
        resp.headers['Content-Type'] = 'application/json; charset=UTF-8'
        if account and password and verify is not None:
            # 检查是否存在用户
            user_check = User.query.filter_by(user_account=account).count()
            if user_check > 0:
                print("用户已存在")
                resp.set_data(jsonify(msg="账号已存在").get_data())
                resp.status_code = StatusCode.CODE_CANT_FINISHT
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
                resp.set_data(jsonify(msg="注册成功").get_data())
                resp.status_code = StatusCode.CODE_FINISTH
                # 请求成功
                return resp
        else:
            resp.set_data(jsonify(msg="格式错误").get_data())
            resp.status_code = StatusCode.CODE_SYTAX_ERROR
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
        resp.headers['Content-Type'] = 'application/json; charset=UTF-8'
        
        if account and password is not None:
            user = User.query.filter_by(user_account=account).first()
            if user:
                user_password = user.user_password
                if password == user_password:
                    resp.set_data(jsonify(msg='登陆成功').get_data())
                    resp.status_code = StatusCode.CODE_FINISTH
                    return resp
                else:
                    resp.set_data(jsonify(mgs="账号错误").get_data())
                    resp.status_code = StatusCode.CODE_UNDERSTAND_REFUSE
                    # 理解客户段请求，但是拒绝
                    return resp

            else :
                resp = make_response(jsonify(msg="用户不存在").get_data())
                resp.status_code = StatusCode.CODE_CANT_FINISHT
                # 服务器无法根据客户端请求的内容特性完成请求
                return resp
    
    @bp.route("/user/addhistory",methods=["POST"])
    def add_history():
        user_account = request.form.get('account')
        news_id = request.form.get('news_id')
        resp = make_response()
        if user_account and news_id is not None:
            user = User.query.filter_by(user_account=user_account).first()
            if user:
                user_id = user.user_id
                time = datetime.datetime.now()
                history = History(user_id=user_id,
                                  news_id=news_id,
                                  history_time=time)
                db.session.add(history)
                db.session.commit()
                resp.set_data(str({'msg':"历史记录创建成功"}))
                resp.status_code = StatusCode.CODE_FINISTH
            else:
                resp.set_data(str({'msg':"用户不存在"}))
                resp.status_code = StatusCode.CODE_FINISTH
        else:
            resp.set_data(str({'msg':"请求格式错误"}))
            resp.status_code = StatusCode.CODE_SYTAX_ERROR
        resp.headers['Content-Type'] = "application/json; charset=UTF-8"
        return resp
        
    
    
    return bp


