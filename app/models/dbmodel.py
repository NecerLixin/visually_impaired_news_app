from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
import os
import json
from tqdm import tqdm
from app import db

# 创建数据库模型类
class News(db.Model):
    # 新闻表
    __tablename__ = 'news'
    news_id = db.Column(db.Integer, primary_key=True)  # 设置主键，能够自动增长
    news_category = db.Column(db.String(32))
    news_time = db.Column(db.String(32))
    new_img_url = db.Column(db.String(64))
    page_url = db.Column(db.String(64))
    source = db.Column(db.String(64))
    tag = db.Column(db.String(32))
    news_title = db.Column(db.String(32))
    news_author = db.Column(db.String(32))
    news_date = db.Column(db.String(32))

class User(db.Model):
    # 用户表
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_count = db.Column(db.String(32), unique=True)
    user_password = db.Column(db.String(32))
    create_time = db.Column(db.DateTime)


class History(db.Model):
    # 历史记录表
    __tablename__ = 'history'
    history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    news_id = db.Column(db.Integer, db.ForeignKey(News.news_id))
    history_time = db.Column(db.DateTime)


class Collection(db.Model):
    # 收藏表
    __tablename__ = 'collection'
    collection_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    news_id = db.Column(db.Integer, db.ForeignKey(News.news_id))
    collection_time = db.Column(db.DateTime)



# if __name__ == "__main__":
#     with app.app_context():
#         # 清除所有表
#         db.drop_all()
#         # 创建所有表
#         db.create_all()
#         with open('samples/news_all.json') as f:
#             data = json.load(f)
#         for sample in tqdm(data,desc='数据库存储'):
#             if 'content' in sample:
#                 news = News(
#                     news_category = sample['category'],
#                     news_time = sample['time'],
#                     new_img_url = sample['item_img_url'],
#                     page_url = sample['page_url'],
#                     source = sample['source'],
#                     tag = sample['tag'],
#                     news_title = sample['title'],
#                     news_author = sample['author']
#                 )
#                 db.session.add(news)
#         db.session.commit()
#         print(app.root_path)

#         # 创建对象 插入数据
