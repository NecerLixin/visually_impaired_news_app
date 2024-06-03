from flask import Blueprint, jsonify, make_response, request
from app.crawlers.scrapy3 import news_storage
from app.models.dbmodel import *
import datetime
from .utils import StatusCode,get_brief


def create_blueprint_users():
    bp = Blueprint('users',__name__)
    @bp.route('/users/register',methods=['POST'])
    def register():
        data = request.get_json()
        account = data.get('account')
        password = data.get('password')
        # verify = request.form.get('vertify')
        date = datetime.date.today()
        resp = make_response()
        resp.headers['Content-Type'] = 'application/json; charset=UTF-8'
        if account and password is not None:
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
        
        data = request.get_json()
        account = data.get('account')
        password = data.get('password')
        resp = make_response()
        
        
        if account and password is not None:
            user = User.query.filter_by(user_account=account).first()
            if user:
                user_password = user.user_password
                if password == user_password:
                    resp.set_data(jsonify(msg='登陆成功').get_data())
                    resp.status_code = StatusCode.CODE_FINISTH
                else:
                    resp.set_data(jsonify(mgs="密码错误").get_data())
                    resp.status_code = StatusCode.CODE_UNDERSTAND_REFUSE
                    # 理解客户段请求，但是拒绝

            else :
                resp = make_response(jsonify(msg="用户不存在").get_data())
                resp.status_code = StatusCode.CODE_CANT_FINISHT
                # 服务器无法根据客户端请求的内容特性完成请求
            resp.headers['Content-Type'] = 'application/json; charset=gzip'
        else:
            resp.set_data(jsonify(msg="未知错误").get_data())
        return resp
            
    
    @bp.route("/users/addhistory",methods=["POST"])
    def add_history():
        data = request.get_json()
        user_account = data.get('account')
        news_id = data.get('news_id')
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
                resp.set_data(jsonify(msg="历史记录创建成功").get_data())
                resp.status_code = StatusCode.CODE_FINISTH
            else:
                resp.set_data(jsonify(msg="用户不存在").get_data())
                resp.status_code = StatusCode.CODE_FINISTH
        else:
            resp.set_data(jsonify(msg="请求格式错误").get_data())
            resp.status_code = StatusCode.CODE_SYTAX_ERROR
        resp.headers['Content-Type'] = "application/json; charset=UTF-8"
        return resp
        
    @bp.route('/users/gethistory',methods=['GET'])
    def get_history():
        user_account = request.args.get('account')
        user_id = User.query.filter_by(user_account=user_account).first().user_id
        history_list = History.query.filter_by(user_id=user_id).order_by(History.history_time.desc()).all()
        resp = make_response()
        if history_list:
            history_news_id = [item.news_id for item in history_list]
            # case_statement = db.case(
            #     *[(News.news_id == news_id, index) for index, news_id in enumerate(history_news_id)],
            #     else_=len(history_news_id)
            # )
            # news_list = News.query.filter(News.news_id.in_(history_news_id)).order_by(case_statement).all()
            history_data  = []
            for i in range(len(history_list)):
                news = News.query.filter_by(news_id=history_news_id[i]).first()
                content = json.loads(news.news_content)
                brief = get_brief(content)
                sample = {
                          "history_time":history_list[i].history_time,
                          "title":news.news_title,
                          "img_url":news.news_img_url,
                          "news_brief":brief,
                          "news_id":news.news_id
                          }
                history_data.append(sample)
            resp.set_data(jsonify(history_data).get_data())
            resp.status_code = StatusCode.CODE_FINISTH
        else:
            resp.set_data(jsonify(msg="无历史记录").get_data())
            resp.status_code = StatusCode.CODE_UNDERSTAND_REFUSE
        resp.headers['Content-Type'] = "application/json; charset=utf-8"
        return resp
    
    return bp
