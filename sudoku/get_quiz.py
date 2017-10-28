#!/usr/bin/env python3
# coding: utf-8

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'http://www.oubk.com/DailySudoku/17465/5'
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')
    s = ''
    for row in range(1, 10):
        for column in range(1, 10):
            value = soup.select('input#k{col}s{row}'.format(row=row, col=column))[0]['value']
            number = 0 if value == '' else int(value)
            s += str(number)
        s += '\n'
    with open('aaa', 'w') as f:
        f.write(s)
