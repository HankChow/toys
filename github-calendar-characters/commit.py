#!/usr/bin/env python3
# coding: utf-8

import os
import requests
from bs4 import BeautifulSoup
from characters import *
from pprint import pprint

class gcc(object):
    
    def __init__(self, chars):
        self.char_width = 5
        self.github_username = 'HankChow' 
        self.chars = chars
        self.concatted = self.list_concat(list(map(self.bitmap2list, list(self.chars))))

    def bitmap2list(self, char):
        names = globals()
        hor_bitmap = names['chr_{c}'.format(c=char)].split('\n')[1:-1]
        ver_bitmap = []
        for i in range(self.char_width):
            ver_bitmap.append(''.join(list(map(lambda x: x[i], hor_bitmap))))
        bool_list = list(map(lambda x: list(map(lambda y: True if y == '0' else False, list(x))), ver_bitmap))
        flat = lambda x: [y for l in x for y in flat(l)] if type(x) is list else [x]
        flatten = flat(bool_list)
        return flatten
    
    def list_concat(self, lists):
        split = [False] * 7
        concatted = lists[0]
        for l in lists[1:]:
            concatted.extend(split)
            concatted.extend(l)
        return concatted
    
    def get_dates(self):
        github_url = 'https://github.com/{username}'.format(username=self.github_username)
        page = requests.get(github_url).text
        soup = BeautifulSoup(page, 'lxml')
        return list(map(lambda x: x['data-date'], soup.find_all('rect', class_='day')[:len(self.concatted)]))

    def do_push(self):
        if int(os.popen('git status >> /dev/null; echo $?').read().strip()) == 0:
            os.system('touch temp.txt')
            changed = 0
            dates = self.get_dates()
            for i in range(len(self.concatted)):
                if self.concatted[i]:
                    changed += 1
                    os.system('echo "{c}" > temp.txt'.format(c=changed))
                    os.system('git add temp.txt')
                    os.system('git commit -m "{c}" --date="{d} 12:00 +0800"'.format(c=changed, d=dates[i]))
            os.system('git push -u origin master')

if __name__ == '__main__':
    pass
