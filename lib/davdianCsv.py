#!/usr/bin/env Python
# -*- coding:utf-8 -*-

import csv
import random


class ReaderCsv:
    ''' csv文件 '''

    # datafile = '/Users/dabenchen/Documents/davdian_python/test_api_dvd/data/test_user.csv'

    items = []
    idx = 0

    def __init__(self, datafile):
        self._loadCsv(datafile)

    # 封装读文件方法
    def _loadCsv(self, datafile):

        # datafile = '/Users/dabenchen/Documents/davdian_python/test_api_dvd/data/test_user.csv'
        self.items = []
        with open(datafile, 'rb') as fd:
            reader = csv.reader(fd)
            print reader

            lines = [line for line in reader]
            length = len(lines)
            idx = 1

            header = lines[0]
            while idx < length:
                data = lines[idx]
                self.items.append(dict(zip(header, data)))
                idx += 1

            #for arr in reader:
            #    self.items.append({'mobile':arr[0], 'password':arr[1]})
        self.idx = 0

    # 封装取下一个数据方法
    def next(self, safe = False):
        if self.idx >= len(self.items):
            if not safe:
                return False
            else:
                self.idx = 0
        index = self.idx
        self.idx += 1
        return self.items[index]

    def current(self):
        if self.idx >= len(self.items):
            return False
        return self.items[self.idx]

    # 封装重置方法
    def reset(self):
        self.idx = 0

    # 封装随机
    def random(self):
        length = len(self.items)
        sea = random.randint(0, length - 1)
        return self.items[sea]

    # 封装取文件方法
    def randCsv(self):
        return self.user[0]



if __name__ == '__main__':
    # reader = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/data/test_user.csv')
    print reader.next()
    print reader.next()
    # print ReaderCsv.randCsv

