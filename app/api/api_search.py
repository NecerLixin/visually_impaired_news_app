from flask import blueprints,request,jsonify,make_response
from .utils import get_brief,StatusCode
from app.models.dbmodel import *



def create_blueprint_search():
    bp = blueprints.Blueprint('search',__name__)
    @bp.route('/search',methods=['GET'])
    def seaarch():
        content = request.args.get('q')
        if not content:
            return jsonify({'error': 'No search query provided'}), 400
        news_list = News.query.filter(
            News.news_title.ilike(f'%{content}%') | News.news_content.ilike(f'%{content}%')
        ).all()
        if len(news_list) == 0:
            return jsonify(msg="无搜索结果",code=2), StatusCode.CODE_CANT_FINISH
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
    return bp