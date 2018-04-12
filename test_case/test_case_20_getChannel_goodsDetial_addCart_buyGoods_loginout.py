#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''
test_case_20_getChannel_goodsDetail_addCart_buyGoods_loginout.py
# 登录 -> 二级菜单 -> 随机商品 -> 商品详情页 -> 加入购物车 -> 购物车结算 -> 订单确认 -> 生成订单
'''

import requests
import unittest
import urllib,urllib2
import csv
import json
import re
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from requests.sessions import Session
from nose.tools import *
from lib.davdianSession import DavdianSession
from lib.davdianCsv import ReaderCsv


# 创建测试
class getChannel_getCart_buy(unittest.TestCase):

    '''获取user_csv'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')
    '''获取test_menu.csv'''
    menus = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_menu.csv')


    # ======执行测试=======
    def setUp(self):
        print u'-----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')


    # ============测试case================
    '''以下是: 二级菜单 -> [随机商品] -> 商品详情页 -> 加入购物车 -> 订单确认页 -> 去支付 -> 生成订单'''
    def action_getChannel_getCart_buy(self, menu_id=None):

        # 请求二级菜单页第一屏
        print u'二级菜单页'
        param = {'menuId':menu_id['menuId']}
        data = self.session.api('/api/mg/sale/channel/getPageFirst', param)

        feedList = data['data']['feedList']
        contents = []
        for item in feedList:
            if not item.has_key('body') or not item['body'].has_key('dataList'):
                continue
            if len(item['body']['dataList']) < 0:
                continue

            dataList = item['body']['dataList']
            for data in dataList:
                if not data.has_key('command'):
                    continue
                if re.match(r'^/\d+.html', data['command']['content']):
                    contents.append(data['command']['content'])
        print "DEBUG\t[%s][%s]" % (u'contents', contents)

        length = len(contents)
        print "DEBUG\t[%s][%s]" % (u'length', length)
        while True:
            randIndex = random.randint(0, length - 1)
            content = re.findall(r"\d+\d*", goodsIdurl)[0]
            print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)


            # 请求商品详情页
            print u'商品详情页'
            param = {'goodsId': goodsId}
            data = self.session.api('/api/mg/good/info/detail', param)
            self.assertEqual(int(data['code']), 0, data['data'])

            # 判断普通商品/多规格商品
            basis = data['data']['basis']
            goodsName = basis['goodsName']
            print goodsName
            if not basis.has_key('childs'):
                return (False, '')
            if len(basis['childs']) < 0:
                return (False, '')
            # 取出childs -> list -> title
            childs = basis['childs']
            if not childs.has_key('list') or len(childs['list']) == 0:
                return (False, '')
            list = childs['list'][0]
            title = childs['list'][0]['title']
            print title
            extra = data['data']['extra']
            if not extra.has_key('dataList') or len(extra['dataList']) == 0:
                return (False, '')
            dataList = extra['dataList'][0]
            sales = dataList['sales']['goodsStocks']
            status = dataList['status']['onSale']
            print sales, status
            # 判断sales大于0，字符串需要转换成int
            if int(sales) > 0:
                print sales
                break
        # 多规格商品拼接: goodsName + title
        goodsNames = goodsName + '_' + title
        print goodsNames


        # 请求
    