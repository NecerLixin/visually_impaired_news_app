from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
import os

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

class Config:
    SQLALCHEMY_DATABASE_URL = prefix + os.path.join(app.root_path,'news.db')

app.config.from_object(Config)

# 将SQLAlchemy和app绑定起来
db = SQLAlchemy(app)

# 创建数据库模型类
class News(db.Model):
    # 新闻表
    __tablename__ = 'news'
    news_id = db.Column(db.Integer,primary_key=True) # 设置主键，能够自动增长
    news_category = db.Colum(db.String(32)) 
    news_time = db.Colum(db.DateTime)
    new_img_url = db.Colum(db.String(64))
    page_url = db.Colum(db.String(64))
    source = db.Colum(db.String(64))
    tag = db.Colum(db.String(32))

class User(db.Model):
    # 用户表
    __tablename__ = 'users'
    user_id = db.Colum(db.Integer,primary_key=True)
    user_count = db.Colum(db.String(32),unique=True)
    user_password = db.Colum(db.String(32))
    create_time = db.Colum(db.DateTime)

class History(db.Model):
    # 历史记录表
    __tablename__ = 'history'
    history_id = db.Colum(db.Integer,primary_key=True)
    user_id = db.Colum(db.Integer,db.ForeignKey(User.user_id))
    news_id = db.Column(db.Integer,db.ForeignKey(News.news_id))
    history_time = db.Colum(db.DateTime)

class Collection(db.Model):
    # 收藏表
    __tablename__ = 'collection'
    collection_id = db.Colum(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey(User.user_id))
    news_id = db.Column(db.Integer,db.ForeignKey(News.news_id))
    collection_time = db.Colum(db.DateTime)
     
    
if __name__ == "__main__":
    # 清除所有表
    db.drop_all()
    # 创建所有表
    db.create_all()
    
    # 创建对象 插入数据