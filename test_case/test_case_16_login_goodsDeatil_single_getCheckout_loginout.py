#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''
test_case_16_login_goodsDeatil_single_getCheckout_loginout.py       # 普通商品
# 步骤
    a. 搜索普通商品
    b. 搜索结果
    c. 商品详情页
    d. 判断是普通商品、多规格商品
        e.1 普通商品:
            e.1.1 判断"childs"字段列表是否为空  *空列表==普通商品
            e.1.2 判断"childs"字段列表是否为空  *不是空列表==多规格商品     **遍历childs -> list -> 随机goodsId

            e.1.3 判断"extra -> dataList字段    *遍历dataList字段，随机goodsId   判断**goodsStocks大于0, onSale等于1**    --多规格
            e.1.4 判断"extra -> dataList字段"   判断*goodsStocks大于0, onSale等于1      --普通商品
    f. /checkout.html

    # 登录 -> 搜索 -> 商品详情(普通) -> 立即购买 -> 订单确认页 -> 退出登录【卖家/卖家游客(登录)】 
'''

import requests
import unittest
import urllib,urllib2
import csv
import random
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from requests.sessions import Session
from nose.tools import *
from lib.davdianSession import DavdianSession
from lib.davdianCsv import ReaderCsv


# 创建测试
class single_getChecout(unittest.TestCase):

    # 获取test_user.csv
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')
    # 获取test_search_single_goods.csv
    searchs = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_search_single_goods.csv')


    # 设置初始化
    def setUp(self):
        print u'-----测试开始-----'

        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')

    

    # ===================测试case====================
    '''以下: 搜索商品 -> 商品详情页 -> 立即购买 -> 订单确认页 '''
    def action_single_getCheckout(self, keywords=None):

        # 请求搜索接口
        print u'首页搜索'
        data = self.session.api('/api/mg/sale/index/getSearch')
        self.assertEqual(int(data['code']), 0, data['data'])

        # 搜索结果
        print u'搜索结果'
        param = {'keywords':keywords['keywords'], 'h5Platform': keywords['h5Platform'], 'pageIndex': keywords['pageIndex'], 'pageSize': keywords['pageSize'], 'sort': keywords['sort']}
        data = self.session.api('/api/mg/sale/search/getGoods', param)
        self.assertEqual(int(data['code']), 0, data['data'])

        # 搜索结果取出goodsId -> 随机goodsId(商品详情)
        
