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

class scrapy:
    def __init__(self,url_dict) -> None:
        self.url_dict = url_dict
        nest_asyncio.apply()
    
    async def fetch_webpage(url):
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
        content = asyncio.get_event_loop().run_until_complete(fetch_webpage(origin_url))
        html = etree.HTML(content,parser=etree.HTMLParser())
        node_list = html.xpath('//*[@id="newslist"]/li')
        url_list = []
        for node in node_list:
            page_url = node.xpath('div[@class="image"]/a/@href')[0]
            image_url = node.xpath('div[1]/a/img/@data-echo')[0]
            url_list.append({'page_url':page_url,'image_url':image_url})
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
        title = html.xpath('//*[@id="title_area"]/h1/text()')[0]
        tag = page_url.split('/')[-1].split('.')[0]
        time = html.xpath('//*[@id="title_area"]/div[1]/text()[2]')[0]
        time = ' '.join(time.split()[1:])
        source = html.xpath('//*[@id="title_area"]/div[1]/a/text()')[0]
        # 处理news content
        news_img_nodes = html.xpath('//*[@id="content_area"]/p[contains(@class,"photo") and contains(@style,"text") and img]')
        news_img_desc_nodes = html.xpath('//*[@id="content_area"]/p[contains(@class,"photo") and contains(@style,"text") and not(*)]')
        news_content_nodes = html.xpath('//*[@id="content_area"]/p')
        content = []
        for node in news_content_nodes:
            if node in news_img_nodes: #取出图片链接
                img_url = 'https:' + node.xpath('img/@src')[0]
                content.append({'type':'img_url','data':img_url})
            elif node in news_img_desc_nodes:
                img_desc = node.xpath('text()')[0].strip()
                content.append({'type':'img_desc','data':img_desc})
            else:
                text = node.xpath('text()')[0].strip()
                if text == "":
                    text = node.xpath('strong/text()')[0]
                    content.append({'type':'text-blod','data':text})
                else:
                    content.append({'type':'text','data':text})
        author = html.xpath('//*[@id="page_body"]/div[1]/div[3]/div[1]/span/text()')
        news_info = dict()
        news_info['title'] = title
        news_info['tag'] = tag
        news_info['time'] = time
        news_info['content'] = content
        news_info['author'] = author
        return news_info