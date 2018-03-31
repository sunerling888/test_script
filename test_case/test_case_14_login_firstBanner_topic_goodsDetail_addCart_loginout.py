#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''
test_case_14_login_firstBanner_topic_goodsDetail_addCart_loginout.py
登录 -> 首页banner专题 -> 【随机专题商品id】 -> 加入购物车（效验商品id,效验商品数量）-> 退出登录【卖家/买家/游客】
'''

import requests
import unittest
import urllib,urllib2
import csv
import json
import random
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from requests.sessions import Session
from nose.tools import *
from lib.davdianSession import DavdianSession
from lib.davdianCsv import ReaderCsv


# 创建测试
class firstBanner_addCart(unittest.TestCase):

    '''获取test_user.csv文件'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')
    # users = ReaderCsv('/home/xiaoqiang.li/scripts/release_li/test_api_dvd/test_data/test_user.csv')
    topics = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_topic.csv')

    # =====执行测试======
    def setUp(self):
        print u'-----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')



    # ==============测试case===================
    '''以下是: 登录 -> 首页banner -> 专题页 -> [随机专题页商品id] -> 商品详情页 -> 加入购物车(效验商品id,数量) -> 退出登录【卖家/买家/游客】'''
    def action_firstBanner_addCart(self, topicId=None):
        '''
        # 请求首页第一屏
        print u'首页第一屏'
        data = self.session.api('/api/mg/sale/index/getPageFirst')

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
                m = re.match(r'^/.+\?topicId=(\d+)&', data['command']['content'])
                if m:
                    topic_Id = m.group(1)
                    contents.append(topic_Id)
        print "DEBUG\t[%s][%s]" % (u'contents', contents)

        length = len(contents)
        print "DEBUG\t[%s][%s]" % (u'length', length)

        randIndex = random.randint(0, length - 1)
        topicId = contents[randIndex]
        print "DEBUG\t[%s][%s]" % (u'topicId', topicId)
        '''

        
        # 请求首页banner专题页
        print u'首页banner专题'
        print topicId
        param = {'topicId': topicId['topicId']}
        data = self.session.api('/api/mg/sale/topic/getTopicInfo?15224819553866', param)
        self.assertEqual(int(data['code']), 0, data['data'])
        
        #print json.dumps(data)
        print type(data)

        

        topicContent = data['data']['topicContent']
        # print type(topicContent)
        # 返回的是字符串，先loads转换成对象
        topicContent = json.loads(topicContent)
        # print type(topicContent)
        # 取下标第4个
        # print topicContent['list'][4]
        
        goodsIds = topicContent['list'][4]['goods']
        print goodsIds
        '''
        goodsIds = []
        for item in topicContent:
            if 'list' not in item :
                continue
            goodsIds.append((int)(item['list'][4]['goods']))

        print goodsIds
        '''
        return True
        

    # =============执行case===============
    def test_01_seller_firstBanner_addCart(self):
        print u'卖家身份:'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        topicId = self.topics.random()
        ret = self.action_firstBanner_addCart(topicId)
        self.assertTrue(ret)
