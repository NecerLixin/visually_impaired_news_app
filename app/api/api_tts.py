from flask import blueprints,request,jsonify,make_response
from .utils import get_content,StatusCode
from app.models.dbmodel import *
from app.models.ifly_tts import TestTask,do_create,do_query
import json
import requests

config_setting = json.load(open('app/config_setting.json'))
project_path = config_setting['project_path']
HOST = "api-dx.xf-yun.com"
APP_ID = config_setting['ifly_key']['APPID']
API_KEY = config_setting['ifly_key']['APIKey']
API_SECRET = config_setting['ifly_key']['APISecret']
AUDIO_FOLDER = 'source'


def create_blueprint_ttsf():
    bp = blueprints.Blueprint('tts',__name__)
    @bp.route('/tts',methods=['GET'])
    def tts():
        news_id = request.args.get('id')
        print(f'tts,id={news_id}')
        news = News.query.filter_by(news_id=news_id).first()
        content = json.loads(news.news_content)
        title = news.news_title
        content_text = get_content(content,title)
        file_name = f'{news_id}.mp3'
        file_path = os.path.join(AUDIO_FOLDER, file_name)
        file_path = os.path.join(project_path,file_path)
        if os.path.exists(file_path):
            print('音频文件已存在')
            return jsonify(msg="音频文件已经存在成功"), StatusCode.CODE_FINISTH
        task_id = do_create(content_text)
        if task_id:
            query_result = do_query(task_id)
            # 4、下载到本地
            Download_addres = query_result
            if Download_addres == None:
                print("下载地址为空")
                return jsonify(msg="失败"), StatusCode.CODE_CANT_FINISHT
            f = requests.get(Download_addres)
            # 下载文件，根据需要更改文件后缀
            
            # filename = "./tts.mp3"
            with open(file_path, "wb") as code:
                code.write(f.content)
            if file_path:
                print("\n音频保存成功！")
            return jsonify(msg="文字转语音成功"), StatusCode.CODE_FINISTH
        else:
            return jsonify(msg="失败"), StatusCode.CODE_CANT_FINISHT
        
        
    
    
    @bp.route('/title2mp3all',methods=['GET'])
    def title2mp3():
        def get_tts_title(news_id,title):
            file_name = f'{news_id}.mp3'
            file_path = os.path.join(AUDIO_FOLDER, file_name)
            file_path = os.path.join(project_path,file_path)
            if os.path.exists(file_path):
                print('音频文件已存在')
                return jsonify(msg="音频文件已经存在成功"), StatusCode.CODE_FINISTH
            task_id = do_create(title)
            if task_id:
                query_result = do_query(task_id)
                # 4、下载到本地
                Download_addres = query_result
                if Download_addres == None:
                    print("下载地址为空")
                    return None
                f = requests.get(Download_addres)
                return f
            
        news_all = News.query.all()
        for news in news_all:
            news_id = news.news_id
            news_title = news.news_title
            title_mp3 = get_tts_title(news_id,news_title)
            if title_mp3 is not None:
                audio = Audio(
                    news_id = news_id,
                    audio_title = title_mp3
                )
                db.session.add(audio)
                db.session.commit()

    return bp