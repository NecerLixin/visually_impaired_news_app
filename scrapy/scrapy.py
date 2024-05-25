import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from lxml import etree
import random
import re
import asyncio
from pyppeteer import launch
import nest_asyncio
import time
import datetime
from tqdm import tqdm

class Scrapy:
    def __init__(self,url_dict) -> None:
        self.url_dict = url_dict
        nest_asyncio.apply()
    
    async def fetch_webpage(self,url):
        """
        使用 Pyppeteer 获取网页内容
        """
        browser = await launch(headless=True)
        page = await browser.newPage()
        await page.goto(url)
        content = await page.content()
        await browser.close()
        return content
    
    def get_random_headers(self)->dict:
        """
        随机生成一个header，用于伪造浏览器

        Returns:
            dict: 返回一个浏览器header
        """
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]

        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",  # Do Not Track Request Header
            "Accept-Encoding": "gzip, deflate, br"
        }
        return headers
    
    def get_url_list(self,origin_url:str,date:str)->list:
        """
        根据源页面的url获取源页面所有新闻的url,获取的新闻的url格式为：
        https://news.cctv.com/year/month/day/abcdfjafa.shtml
            \n year 例如：2024
            \n month 例如：05
            \n day 例如：22
        Args:
            origin_url (str): 央视新闻网首页以及其各种分类界面
            date (str): 日期字符串，例如 "2024/05/22"
        Returns:
            list: 包含所有新闻界面url和首页图片url的一个列表 \n
                [[page_url,img_url],...]
        """
        content = asyncio.get_event_loop().run_until_complete(self.fetch_webpage(origin_url))
        html = etree.HTML(content,parser=etree.HTMLParser())
        node_list = html.xpath('//*[@id="newslist"]/li')
        url_list = []
        for node in node_list:
            page_url = node.xpath('div[@class="image"]/a/@href')[0]
            image_url = node.xpath('div[1]/a/img/@data-echo')[0]
            if "photo.cctv.com" not in page_url:
                url_list.append({'page_url':page_url,'img_url':image_url})
        return url_list
    
    
    def page_parse(self,page_url:str)->dict:
        """
        对每个页面进行解析，获取数据
        需要的数据有：新闻标题、来源、时间、内容、作者信息

        Args:
            page_url (str): 新闻页面URL

        Returns:
            dict: 每个新闻界面的数据
            {"title":新闻标题(str),
            "tag":新闻唯一标识(str),
            "time":新闻时间(str),
            "content": [   
                        {
                            "type": text(文本) |text-blod(粗体文本) | imge_url(图片链接) | img_desc(图片描述),
                            "data": text | url
                            },
                            ...
                        ],
            "author": 编辑信息(str)
            }
        """
        response = requests.get(page_url,headers=self.get_random_headers())
        response.encoding = 'utf-8'
        content = response.text
        html = etree.HTML(content,parser=etree.HTMLParser())
        news_content_nodes = []
        try:
            title = html.xpath('//*[@id="title_area"]/h1/text()')[0]
            tag = page_url.split('/')[-1].split('.')[0]
            time = html.xpath('//*[@id="title_area"]/div[2]/text()')
            if len(time) == 0:
                time = html.xpath('//*[@id="title_area"]/div/span[3]/text()')
            #//*[@id="title_area"]/div/span[3]
            else:
                time = time[0]
                time = ' '.join(time.split()[-2:])
            source = html.xpath('//*[@id="title_area"]/div[1]/text()')
            if len(source) == 0:
                source = html.xpaht('//*[@id="title_area"]/div/span[2]/text()')
                # //*[@id="title_area"]/div/span[2]
            else:
                source = source[0].split()[0]
            #//*[@id="title_area"]/div/span[2]
            # 处理news content//*[@id="text_area"]/p[2]
            # //*[@id="text_area"]/p[4]/img
            # //*[@id="content_area"]/p[1]/text()[2]
            news_img_nodes = html.xpath('//*[@id="content_area" or @id="text_area"]/p[contains(@class,"photo") and contains(@style,"text") and img]')
            news_img_desc_nodes = html.xpath('//*[@id="content_area" or @id="text_area"]/p[contains(@class,"photo") and contains(@style,"text") and not(*)]')
            news_content_nodes = html.xpath('//*[@id="content_area" or @id="text_area"]/p')
        except:
            return {}
       
        content = []
        for node in news_content_nodes:
            if node in news_img_nodes: #取出图片链接
                img_url = 'https:' + node.xpath('img/@src')[0]
                content.append({'type':'img_url','data':img_url})
            elif node in news_img_desc_nodes:
                img_desc = node.xpath('text()')
                if img_desc:
                    img_desc = img_desc[0].strip()
                content.append({'type':'img_desc','data':img_desc})
                # //*[@id="content_area"]/p[1]/strong
            else:
                text_strong = node.xpath('strong/text()')
                if text_strong:
                    text_strong = text_strong[0]
                    content.append({'type':'text-blod','data':text_strong})
                text = node.xpath('text()')
                if text:
                    text = ''.join(text).strip()
                    content.append({'type':'text','data':text})
                    
        author = html.xpath('//*[@id="page_body"]/div[1]/div[3]/div[1]/span/text()')
        if len(author)==0:
            author = ""
        news_info = dict()
        news_info['title'] = title.strip()
        news_info['tag'] = tag
        news_info['time'] = time
        news_info['content'] = content
        news_info['author'] = author
        news_info['source'] = source
        return news_info
    def get_all_kind_page(self,origin_url_dict:dict,date:str)->dict:
        """获得所有分类的新闻的URL，分类包括：国内、国际、经济、社会、法治、文娱、科技、生活、军事

        Args:
            origin_url_dict (dict): {"新闻种类":origin_url,...}
            date (str): year/month/day

        Returns:
            dict: {"新闻种类1":["url1","url2",...],
                "新闻种类1":["url1","url2",...],
                    ....}
        """
        res = []
        for news_kind, origin_url in tqdm(origin_url_dict.items(),desc='新闻种类'):
            url_list = self.get_url_list(origin_url=origin_url,date=date)
            for url_dict in tqdm(url_list,desc='新闻爬取'):
                page_url = url_dict['page_url']
                img_url = url_dict['img_url']
                print(f'page url:{page_url}')
                details = self.page_parse(page_url)
                # sample = dict()
                details['page_url'] = page_url
                details['item_img_url'] = img_url
                details['category'] = news_kind
                res.append(details)
                time.sleep(1)
        return res

if __name__ == "__main__":
    origin_url_dict = json.load(open('scrapy/newsURLdict.json'))
    scrapy = Scrapy(origin_url_dict)
    date = datetime.date.today()
    date = date.strftime("%y/%m/%d")
    res = scrapy.get_all_kind_page(origin_url_dict,date)
    with open('news_all.json','w') as f:
        json.dump(res,f,ensure_ascii=False)
    print(len(res))
    
