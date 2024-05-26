from flask import Flask,jsonify,make_response
import json

app = Flask(__name__)
file_path = "scrapy/news_sample.json"


@app.route('/index')
def index():
    res_content = str(json.load(open(file_path)))
    print(type(res_content))
    response = make_response(res_content)
    response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    return response

if __name__ == "__main__":
    app.run()