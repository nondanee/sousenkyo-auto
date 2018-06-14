# -*- coding: utf-8 -*-
"""
Created on Sat Jun 02 00:30:22 2018

@author: Nzix
"""

#import re
import csv
import requests
from bs4 import BeautifulSoup  

def vote(serial1,serial2,vid):
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    # session.verify = False
    # session.proxies = {'https':'https://127.0.0.1:1080'}
    session.get('https://akb48-sousenkyo.jp/akb/search/results',params = {'t_id': 1})
    response = session.get('https://akb48-sousenkyo.jp/akb/vote',params = {'id': vid})
    
    html = response.text
    soup = BeautifulSoup(html,'lxml')
    
    hash_value = soup.find('input',id='hash').get('value')
    skey_value = soup.find('input',id='skey').get('value')
    
    # hash_value = re.search(r'''name='hash' value='([^']+)'>''',html).group(1)
    # skey_value = re.search(r'''name='s_key' value="([^']+)">''',html).group(1)
    
    response = session.post('https://akb48-sousenkyo.jp/akb/vote',
         data = {'serial1': serial1,'serial2': serial2,'s_key': skey_value,'hash': hash_value,'id': vid}
    )

    # print(response.url)
    # 'https://akb48-sousenkyo.jp/akb/vote/complete'
    # 'https://akb48-sousenkyo.jp/akb/vote/error'
    
    html = response.text
    soup = BeautifulSoup(html,'lxml')
    
    print(soup.find('h1').get_text())
    message = soup.find_all(attrs={'class':'lead'})
    for line in message:
        print(line.get_text().strip())

if __name__ == '__main__':

    with open('input.csv') as f:
        data = list(csv.reader(f))
        for line in data:
            vote(line[0],line[1],line[2])
    
    




