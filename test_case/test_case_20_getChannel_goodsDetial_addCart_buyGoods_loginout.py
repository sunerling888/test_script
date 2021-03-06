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
from bs4 import BeautifulSoup


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
        param = {'menuId': menu_id['menuId']}
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

        randIndex = random.randint(0, length - 1)
        content = contents[randIndex]
        goodsIdurl = contents[randIndex]
        goodsId = re.findall(r"\d+\d*", goodsIdurl)[0]
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)


        # 请求商品详情页
        print u'商品详情页'
        param = {'goodsId': goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        self.assertEqual(int(data['code']), 0, data['data'])

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
        print sales,status
        '''
        # 判断sales大于0，字符串需要转换成int
        if int(sales) > 0:
            print sales
                break
        # 多规格商品拼接: goodsName + title
        goodsNames = goodsName + '_' + title
        print goodsNames
        '''
        # 加入购物车
        print u'加入购物车'
        param = {'goods': urllib.quote(json.dumps({"number":1, "goods_id":goodsId}))}
        print param['goods']
        data = self.session.post('/index.php?c=cart&a=add_to_cart&m=default', urllib.urlencode(param))

        # 请求购物车页面
        print u'购物车页面'
        response = self.session.get('/cart.html?c=cart&a=load')
        # print response


        # 请求订单确认页
        print u'订单确认页'
        if sales == 0 and status != 1:
            return (False, '')
        param = {'goods[0][id]': str(goodsId), 'goods[0][number]': '1'}
        response1 = self.session.get('/checkout.html?rp=goods_detail&rl=checkout' + '&' + urllib.urlencode(param))
        print urllib.urlencode(param)

        #  判断: 游客身份跳转到登录页面
        if response1['body'].find('js/login.js') != -1:
            return (True, response1['body'])

        # print response1['body']
        # 订单页取出addressId,获取addressId的值
        value = 'window.addressId = '
        index = response1['body'].find(value)
        if index == -1:
            return (False, '')
        # print index, len(value)
        add_index = index + len(value)
        for i in response1['body'][add_index:]:
            if i == ';':
                break
            add_index += 1
        # print add_index
        # print response1['body'][(index+len(value)):add_index]
        addressId = response1['body'][(index+len(value)):add_index]
        print u'地址id:', addressId

        # 订单确认页, 取出身份证信息id
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

        # 取出订单确认页，收货人姓名
        result = False
        soup = BeautifulSoup(response1['body'], 'html.parser')
        base_name = soup.find_all("span", class_='name')
        # print base_name
        # 获取good_title里的值
        if len(base_name) > 0:
            base_name = base_name[0].get_text().strip()
            print u'收货人姓名:', base_name
            '''
            if goodsNames == content:
                result = True
            self.assertTrue(result, u'商品不存在!')
            '''
        # return (result, response1['body'])
        

        # 订单确认页，设置不使用红包
        param = {'bonus_id':0}
        response = self.session.get('/checkoutBonus.html?' + urllib.urlencode(param))
        print urllib.urlencode(param)
        # print response
        result = False


        # 去支付，请求vdone页
        print u'订单确认页生成订单'
        param = {'order_id':0, 'bonus_id':0, 'address_id':addressId, 'commission':0, 'idcard':idcard}
        response = self.session.get('/vdone.html?rp=checkout&rl=next' + '&' + urllib.urlencode(param))
        print urllib.urlencode(param)
        print response['body']
        
        # 效验status是否等于0,不等于0打印status,msg
        s = json.loads(response['body'])
        if 'status' in s:
            if s['status'] != 0:
                print "Failed! [status not 0][status:%s][message:%s]" % (s['status'], s['msg'])
                # response.("Failed! [status not 0][status:%s][message:%s]" % (s['status'], s['msg']))
                return False
                
            print "SUCEESS! [status not 0][status:%s][message:%s]" % (s['status'], s['msg'])
        
        return True

    
    # =============执行case==============
    def test_01_seller_getChannel_getCart_buy(self):
        print u'卖家身份: 二级菜单 -> 随机商品 -> 商品详情页 -> 加入购物车 -> 购物车结算 -> 订单确认 -> 生成订单'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        menu_id = self.menus.random()
        ret = self.action_getChannel_getCart_buy(menu_id)
        self.assertTrue(ret)

    
    def test_02_user_getChannel_getCart_buy(self):
        print u'买家身份: 二级菜单 -> 随机商品 -> 商品详情页 -> 加入购物车 -> 购物车结算 -> 订单确认 -> 生成订单'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        menu_id = self.menus.random()
        ret = self.action_getChannel_getCart_buy(menu_id)
        self.assertTrue(ret)

    
    def test_03_no_getChannel_getCart_buy(self):
        print u'游客身份: 二级菜单 -> 随机商品 -> 商品详情页 -> 加入购物车 -> 购物车结算 -> 订单确认 -> 登录(判断是否跳到登录页)'
        menu_id = self.menus.random()
        ret = self.action_getChannel_getCart_buy(menu_id)
        self.assertTrue(ret)
        print ret
        # 取出sess_key
        sess_key = self.session.session
        print sess_key