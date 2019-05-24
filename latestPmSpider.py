#! /home/student/bde19/16081121/Sentiment/python/bin/python
# -*- coding: utf-8 -*-
"""
@decription:
    爬取最新的文章，可以设置在服务器上定时爬取
@author: pone
"""
from requests_html import HTMLSession
import json
import pandas as pd
import requests
import os

OUTPUTDIR = 'pmdocs/'


def artiSpider(url, output_file):
    """
    抓取文章正文
    Parameters
    ----------
    url 文章链接
    output_file 输出文件地址，output_file = output_dir + 文件名

    Returns 正文写入文件
    -------

    """
    session = HTMLSession()
    session.headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36', 'Connection': 'close'}
    r = session.get(url)
    article_text = r.html.xpath(
        '/html/body/div[1]/div[3]/div[1]/div/article/div[5]')[0].text.replace('\n', ' ')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(article_text)


def pmSpiderMain():
    """
    爬取最新的文章
    Returns 最新文章的目录
    -------

    """
    session = HTMLSession()
    r = session.get('http://www.woshipm.com/')
    docs = {'link': [], 'title': [], 'time': [],
            'author': [], 'filename': [], 'category': []}
    for article in r.html.xpath('//div[@class = "postlist-item u-clearfix"]'):
        link = article.find('h2')[0].find('a')[0].attrs['href']
        time = article.xpath('div/div[2]/div/time')[0].text
        title = article.find('h2')[0].find('a')[0].attrs['title']
        author = article.xpath('div/div[2]/div/span[2]/a')[0].text
        category = link.split('/')[3]
        if category == 'active':
            continue
        id = link.split('/')[4].strip('.html')
        filename1 = OUTPUTDIR + category + '/' + id + '.txt'
        filename2 = OUTPUTDIR + 'latest/' + category + id + '.txt'
        if os.path.exists(filename1):
            return docs
        elif os.path.exists(filename2):
            return docs
        else:
            docs['link'].append(link)
            docs['title'].append(title)
            docs['time'].append(time)
            docs['author'].append(author)
            docs['filename'].append(filename2)
            docs['category'].append(category)
            artiSpider(link, filename2)
    for i in range(2, 4):
        r1 = session.get(
            'http://www.woshipm.com/__api/v1/stream-list/page/{}'.format(i))
        r1 = json.loads(r1.content)
        for article in r1['payload'][:]:
            category = article['catslug']
            if category == 'active':
                continue
            time = article['date']  # time
            id = article['id']  # id
            link = article['permalink']  # link
            author = article['author']['name']  # author
            title = article['title']  # title
            filename1 = OUTPUTDIR + category + '/' + str(id) + '.txt'
            filename2 = OUTPUTDIR + 'latest/' + category + str(id) + '.txt'
            if os.path.exists(filename1):
                return docs
            elif os.path.exists(filename2):
                return docs
            else:
                docs['link'].append(link)
                docs['title'].append(title)
                docs['time'].append(time)
                docs['author'].append(author)
                docs['filename'].append(filename2)
                docs['category'].append(category)
                artiSpider(link, filename2)
    pd.DataFrame(docs).to_csv(OUTPUTDIR + 'latest.csv', mode = 'a', header = False, index = False)
    return docs

def notification(urls, titles):
    """
    向手机发送消息通知
    Returns
    -------

    """
    if len(urls) == 0:
        return 0
    headers = {'Content-Type':'application/json'}
    messages = '新增文章：\n'
    for i in range(len(urls)):
        messages += "<a href = {}>{}</a>\n".format(urls[i], titles[i])
    data = {'token':token,'user':usertoken,
            'title':'人人都是产品经理爬虫更新','message':messages,'html':1}
    r = requests.post('https://api.pushover.net/1/messages.json', json = data, headers = headers)

if __name__ == '__main__':
    docs = pmSpiderMain()
    notification(docs['link'],docs['title'])
