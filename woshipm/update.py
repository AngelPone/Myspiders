# -*- coding: utf-8 -*-
"""
@description:
    将每天爬到的文章放在对应的文件夹和CSV中
@author: pone
"""
import os
import requests
import pandas as pd
import re

def updateFile():
    """
    将每天爬到的文章放在对应的文件夹和CSV中
    Returns
    -------

    """
    f = open('pmdocs/latest.csv', encoding = 'utf-8')
    g = f.readline().strip('\n')
    while g != '':
        split_g = g.split(',')
        filename = split_g[0].split('/')[4].strip('.html') + '.txt'
        # 服务器上是9
        numbers = len(open('pmdocs/' + split_g[5] + '.csv', 'r', encoding = 'utf-8').readlines())
        with open('pmdocs/' + split_g[5] + '.csv', 'a', encoding = 'utf-8') as file:
            content = ','.join([str(numbers - 1), split_g[0], split_g[1], split_g[3],
                                 split_g[2], 'pmodocs/' + split_g[5] + '/' + filename])
            file.write(content + '\n')
        os.system('mv pmdocs/latest/' + split_g[5] + filename + ' pmdocs/' + split_g[5] + '/' + filename)
        g = f.readline().strip('\n')

if __name__ == '__main__':
    updateFile()
    f = open('pmdocs/latest.csv','w')
    f.close()