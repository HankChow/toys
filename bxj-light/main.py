#!/usr/bin/env python3
# coding: utf-8

import time
import os
import requests
from bs4 import BeautifulSoup


class lights(object):

    def __init__(self):
        self.block = 'bxj'

    def get_post_id_by_date(self, date=None):
        posts_of_date = []
        target_date = get_today_date() if not date else date
        target_date = '-'.join([target_date[:4], target_date[4:6], target_date[6:]])
        for i in range(1, 2):
            url = 'https://bbs.hupu.com/{}-{}'.format(self.block, i)
            resp = requests.get(url)
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'lxml')
            page_posts = soup.find('ul', class_='for-list').find_all('li')
            if len(page_posts) == 0:
                break
            posts_of_date = list(filter(lambda x: x.find('div', class_='author').find('a', class_=False).text == target_date, page_posts))
            posts_of_date = list(map(lambda x: x.find('div', class_='titlelink').find('a', class_='truetit')['href'][1:-5], posts_of_date))
        return posts_of_date

def get_today_date():
    return time.strftime('%Y%m%d')

if __name__ == '__main__':
    l = lights()
    l.get_post_id_by_date()
