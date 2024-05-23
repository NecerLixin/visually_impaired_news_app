from flask import Flask,request,jsonify

app = Flask(__name__)

#http://127.0.0.1:5000/index?name=llixin&age=21
@app.route("/index")
def index():
    name = request.args.get("name")
    age = request.args.get("age")
    print(name,age)
    return jsonify({'code':200,'xx':name,'content':"你好，这是测试"})



#请求体：xx=123&yy=999
@app.route("/index2",methods=["POST","GET"])
def index2():
    xx = request.form.get("xx") # 获取请求体的数据
    yy = request.form.get("yy")
    print(xx,yy)
    return "成功"


#请求体：{"xx":111,"yy":222}
@app.route("/indexjson",methods=["POST","GET"])
def index3():
    data = request.json
    print(data,type(data))
    return "成功"



@app.route("/home")
def home():
    return "失败"



if __name__ == '__main__':
    app.run()