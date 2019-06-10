#! /home/student/bde19/16081121/Sentiment/python/bin/python
# -*- coding: utf-8 -*-
"""
@author:pone
"""
from requests_html import HTMLSession
import os
import requests
import time
import traceback

DOMAIN = 'http://www.chinadaily.com.cn'
DATAOUTPUT = 'data'
CATE = ['life', 'culture', 'travel', 'sports', 'opinion']


def getSubcate(subcate, skip):
    """获取主要目录下的子目录"""
    url = DOMAIN + '/' + subcate  # 生成分类的URL
    session = HTMLSession()
    r = session.get(url)
    suburls = [i for i in r.html.xpath('/html/body/div[5]/ul')[0].absolute_links
               if i.split('/')[-1] not in skip]
    return suburls


def getSubsubcate(url):
    """获取子目录下的文章链接"""
    session = HTMLSession()
    r = session.get(url)
    docurls = [list(i.absolute_links)[0] for i in r.html.xpath(
        '//*[@id="lft-art"]/div/span[@class = "tw3_01_2_t"]')]
    return docurls


def getDocContent(url):
    session = HTMLSession()
    r = session.get(url)
    text = r.html.xpath('//*[@id="Content"]')[0].text.replace('\n', ' ')
    return text


def main(ranges):
    """主程序

    main: 
        每个子目录下爬取的页面范围
    """
    f = open(os.path.join(DATAOUTPUT, 'other.txt'), 'w')
    skip = ['chinadata', 'top1lists', 'video', 'photo', 'trendwatch']
    # 子目录
    for cate in CATE:
        subcates = getSubcate(cate, skip)
        # 子目录下的多页
        suburls = []
        for subsubcate in subcates:
            suburls += [subsubcate + '/page_' +
                        str(i) + '.html' for i in range(1, ranges)]
        # 对每一页获取所有的子文章链接，并抓取
        print(subcates)
        for url in suburls:
            docurls = getSubsubcate(url)
            for docurl in docurls:
                content = getDocContent(docurl)
                f.write('{}\001{}\001{}\n'.format(cate, docurl, content))


if __name__ == "__main__":
    main(20)
