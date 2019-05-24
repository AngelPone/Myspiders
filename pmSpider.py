#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Pone
@description: 抓取人人都是产品经理的文章，包括正文，标题，作者，发布时间，摘要，并保存在文件里
"""
from requests_html import HTMLSession
import multiprocessing as mp
import time
import pandas as pd
import re
import getopt
import sys
import os

def categSpider(url, output_dir):
    """
    抓取单个目录页，获得链接、标题、作者、时间
    Parameters
    ----------
    url 目录页链接

    Returns 列表，每个元素都是一个字典，包含href、title、author、time等key
    -------

    """
    session = HTMLSession()
    session.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36','Connection':'close'}
    r = session.get(url)
   
     #获取所有信息
    articles = {'href': [], 'title': [],
                'author': [], 'time': [], 'filename': []}

    for article in r.html.xpath('/html/body/div[1]/div[4]/div[1]/div/div[1]/div'):
        articles['href'].append(article.find(
            'h2')[0].find('a')[0].attrs['href'])
        articles['title'].append(article.find(
            'h2')[0].find('a')[0].attrs['title'])
        articles['author'].append(article.xpath(
            'div/div[2]/div/span[2]/a')[0].text)
        articles['time'].append(article.xpath('div/div[2]/div/time')[0].text)
    # 抓取所有的正文
    for i in articles['href']:
        filename = re.findall('\d+\.html', i)[0].strip('.html')
        filepath = output_dir + filename + '.txt'
        while True:
            try:
                f = open(filepath, 'r')
                f.close()
                filename = 'Z' + filename
                filepath = output_dir + filename + '.txt'
            except FileNotFoundError:
                artiSpider(i, output_dir + filename + '.txt')
                break
        articles['filename'].append(filepath)
        time.sleep(0.3)
    return articles


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
    session.headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36','Connection':'close'}
    r = session.get(url)
    article_text = r.html.xpath(
        '/html/body/div[1]/div[3]/div[1]/div/article/div[5]')[0].text.replace('\n', ' ')
    with open(output_file, 'w') as f:
        f.write(article_text)


def pmSpider(category, ranges):
    """
    并行爬取主要抓取程序
    Parameters
    ----------
    category 目录代码
    ranges 爬取的最大页面数

    Returns 所有抓取内容的CSV文件，包含正文文件名、标题、链接、作者、时间
    -------

    """
    suboutputdir = OUTPUTDIR + category
    if not os.path.exists(suboutputdir):
        os.mkdir(suboutputdir)  # 创建子文件夹，如果不存在
    category_urls = [['http://www.woshipm.com/category/{}/page/{}'.format(category, i),suboutputdir + '/']  for i in range(1, int(ranges) + 1)]
    pool = mp.Pool(mp.cpu_count() // 2)
    results = pool.starmap_async(categSpider, category_urls).get() 
   
    # 结果转化为Pandas.DataFrame格式并输出到Csv
    df = pd.DataFrame()
    for i in results:
        df = df.append(pd.DataFrame(i))
    df.to_csv(METADATADIR + category + '.csv')


def main(args):
    try:
        opts, args = getopt.getopt(args, 'c:n:', ['category=', 'numbers='])
    except getopt.GetoptError:
        print('Usage: [-c|--category] <category> [-n|--numbers] <number range>')
        sys.exit()
    for opt, optval in opts:
        if opt in ['-c', '--category']:
            category = optval
        elif opt in ['-n', '--numbers']:
            ranges = optval
    pmSpider(category, ranges)


if __name__ == '__main__':
    OUTPUTDIR = 'pmdocs/'  # 输出文件夹
    METADATADIR = 'pmdocs/'  # 文章信息文件
    main(sys.argv[1:])
