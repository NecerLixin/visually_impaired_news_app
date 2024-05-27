# visually_impaired_news_app_backend

视障人士新闻资讯软件后端代码

## 后端项目部署

## 需要根据本地修改的文件

app文件夹中的config_settings

将`database_path`修改成自己的SQLlite数据库的路径

如果数据库没有根据模型创建表格，设置`database_tables_exist`为false，代码会为数据库自动创建表格

## 运行项目

1. `cd 项目目录`
2. 创建虚拟环境`conda create -n --name env_name python==3.11`
3. 激活虚拟环境`conda activate env_name`
4. 运行`pip install -r requirements.txt`
5. 运行`flask run`

## 接口

1. /crawl， GET 请求
   进行爬虫获取新闻数据，存储到数据库中，每天使用一次即可
2. /api/getnews GET 请求
   从数据库中查询，返回新闻数据
