#!/usr/bin/env python3
# coding: utf-8

from characters import *

CHAR_WIDTH = 5

def bitmap2list(char):
    names = globals()
    hor_bitmap = names['chr_{c}'.format(c=char)].split('\n')[1:-1]
    ver_bitmap = []
    for i in range(CHAR_WIDTH):
        ver_bitmap.append(''.join(list(map(lambda x: x[i], hor_bitmap))))
    bool_list = list(map(lambda x: list(map(lambda y: True if y == '0' else False, list(x))), ver_bitmap))
    return bool_list

if __name__ == '__main__':
    pass
