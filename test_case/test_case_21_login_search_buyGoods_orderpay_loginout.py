#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''
test_case_21_login_search_buyGoods_orderpay_loginout.py
# 登录 -> 搜索商品 -> 商品详情页 -> 购买 -> 订单确认 -> 支付完成
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
from bs4 import BeautifulSoup


# 创建测试
class search_buyGoods_pay(unittest.TestCase):

    '''获取test_user.csv'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')
    '''获取test_search_goods_buy.csv'''
    searchs = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_search_goods_buy.csv')


    
    # ======执行测试=======
    def setUp(self):
        print u'-----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')


    # ============测试case================
    '''以下是:搜索商品 -> 商品详情页 -> 立即购买 -> 订单确认页 -> 支付vdone -> 完成支付'''
    def action_search_buyGoods_pay(self, keywords=None):

        # 请求首页搜索
        print u'首页搜索'
        data = self.session.api('/api/mg/sale/index/getSearch')
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)

        
        # 请求搜索结果
        print u'搜索结果'
        param = {'keywords':keywords['keywords'], 'h5Platform': keywords['h5Platform'], 'pageIndex': keywords['pageIndex'], 'pageSize': keywords['pageSize'], 'sort': keywords['sort']}
        data = self.session.api('/api/mg/sale/search/getGoods', param)
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)

        # 取出goodsId,随机goodsId
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
                if not data['command'].has_key('content'):
                    continue
                if re.match(r'^/\d+.html', data['command']['content']):
                    contents.append(data['command']['content'])

        length = len(contents)
        randIndex = random.randint(0, length - 1)
        content = contents[randIndex]

        goodsIdurl = contents[randIndex]
        goodsId = int(re.findall(r"\d+\d*", goodsIdurl)[0])
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)


        # 请求商品详情页
        print u'商品详情页'
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        param = {'goodsId': goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        # print json.dumps(data)

        # 判断普通商品
        basis = data['data']['basis']
        goodsName = basis['goodsName']
        print goodsName
        if not basis.has_key('childs'):
            return (False, '')
        if len(basis['childs']) > 0:
            return (False, '')
        extra = data['data']['extra']
        if not extra.has_key('dataList') or len(extra['dataList']) == 0:
            return (False, '')
        dataList = extra['dataList'][0]
        sales = dataList['sales']['goodsStocks']
        status = dataList['status']['onSale']
        print u'商品库存:', sales
        print u'是否在售:', status
     

        # 请求订单确认页
        if sales == 0 and status != 1:
            return (False, '')
        param = {'goods[0][id]': str(goodsId), 'goods[0][number]': '1'}
        response1 = self.session.get('/checkout.html?rp=goods_detail&rl=checkout' + '&' + urllib.urlencode(param))
        print urllib.urlencode(param)

        # 游客身份跳转到登录
        if response1['body'].find('js/login.js') != -1:
            return (True, response1['body'])

        
        # 订单页取出addressId，获取addressId的值
        value = 'window.addressId = '
        index = response1['body'].find(value)
        if index == -1:
            return (False, '')
        add_index = index + len(value)
        for i in response1['body'][add_index:]:
            if i == ';':
                break
            add_index += 1
        addressId = response1['body'][(index+len(value)):add_index]
        print u'地址id:', addressId

        # 订单页取出身份证信息id
        value2 = 'idcard_id = '
        index = response1['body'].find(value2)
        if index == -1:
            return (False, '')
        add_index = index + len(value2)
        for j in response1['body'][add_index:]:
            if j == ';':
                break
            add_index += 1
        idcard = response1['body'][(index+len(value2)):add_index]
        print u'身份信息id:', idcard

        # 订单确认页取出收货人姓名
        result = False
        soup = BeautifulSoup(response1['body'], 'html.parser')
        base_name = soup.find_all("span", class_='name')
        if len(base_name) > 0:
            base_name = base_name[0].get_text().strip()
            print u'收货人姓名:', base_name

        # 订单确认页，取出商品金额
        result = False
        soup = BeautifulSoup(response1['body'], 'html.parser')
        good_price = soup.find_all("div", class_='good_price')
        #print good_price[0]
        dav_price = good_price[0].find_all("span", class_='dav-price')
        # print dav_price[0]
        dav_small = dav_price[0].find_all("span", class_='dav-small')
        small_price = dav_small[0].get_text()
        # print small_price
        dav_money = dav_price[0].get_text()
        # print dav_money
        # print dav_money[dav_money.find(small_price)+1:].strip()
        goods_price = dav_money[dav_money.find(small_price)+1:].strip()
        print u'商品金额:', goods_price
        
        # 订单确认页,取出商品数量
        result = False
        soup = BeautifulSoup(response1['body'], 'html.parser')
        goods_prices = soup.find_all("div", class_='good_price')
        # print goods_prices
        goods_price_spans= goods_prices[0].find_all("span")
        goods_number = goods_price_spans[-1].get_text().strip()
        number = 0
        number_index = goods_number.find(' ')
        if number_index == -1:
            return False
        for char in goods_number[number_index+1:]:
            if char == ' ':
                number_index += 1
            else:
                break
        number = goods_number[number_index+1:]
        print u'商品数量:', number

        # 订单确认页，取出返现金额
        result = False
        soup = BeautifulSoup(response1['body'], 'html.parser')
        confirm = soup.find_all("div", class_='confirm_tips')
        # print confirm[0]
        confirm_money = confirm[0].find("span").get_text()
        print u'返现金额:', confirm_money

        # 订单确认页，设置不使用红包
        param = {'bonus_id':0}
        response = self.session.get('/checkoutBonus.html?' + urllib.urlencode(param))
        print urllib.urlencode(param)
        

        # 去支付,请求vdone页
        print u'订单确认页生成订单'
        param = {'goods[0][id]': str(goodsId), 'goods[0][number]':number, 'goods[0][price]': goods_price, 'goods[0][act_id]':0, 'goods[0][act_stime]':0, 'goods[0][act_etime]':0, 'goods[0][price_act_id]':0, 'goods[0][price_act_type]':0, 'goods[0][income]':confirm_money, 'goods[0][pay_start_time]':0, 'goods[0][pay_start_time_format]':0, 'goods[0][pay_end_time]':0, 'goods[0][discount_price]':0, 'goods[0][advance_price]':0, 'goods[0][advance_price_one]':0,'goods[0][end_price]':0, 'goods[0][limit_num]':0, 'order_id':0, 'bonus_id':0, 'address_id':addressId, 'commission':0, 'idcard':idcard}
        response = self.session.get('/vdone.html?rp=checkout&rl=next' + '&' + urllib.urlencode(param))
        print urllib.urlencode(param)
        print response['body']

        # 效验status是否等于0,不等于0打印status,msg
        s = json.loads(response['body'])
        if 'status' in s:
            if s['status'] != 0:
                print "Failed! [status not 0][status:%s][message:%s]" % (s['status'], s['msg'])
                return False
            
            print "SUCEESS! [status not 0][status:%s][message:%s]" % (s['status'], s['msg'])
        return True



    # ============执行case==============
    def test_01_seller_search_buyGoods_pay(self):
        print u'卖家身份:'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        query = self.searchs.random()
        ret = self.action_search_buyGoods_pay(query)
        self.assertTrue(ret)


