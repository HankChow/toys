#!/usr/bin/env python3
# coding: utf-8

import requests
import sys
from bs4 import BeautifulSoup

if __name__ == '__main__':
    if 'page' not in sys.argv:
        url = 'http://www.oubk.com/DailySudoku/17465/5'
        page = requests.get(url).text
    else:
        with open('page') as f:
            page = f.read()
    soup = BeautifulSoup(page, 'lxml')
    s = ''
    for row in range(1, 10):
        for column in range(1, 10):
            value = soup.select('input#k{col}s{row}'.format(row=row, col=column))[0]['value']
            number = 0 if value == '' else int(value)
            s += str(number)
        s += '\n'
    if 'page' in sys.argv:
        with open('ddd', 'w') as f:
            f.write(s)
    else:
        with open('aaa', 'w') as f:
            f.write(s)
