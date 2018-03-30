#!/usr/bin/env Python
# -*- coding:utf-8

'''
redsis_info_test.py    监听redis队列,自动执行测试脚本
'''


import redis
import json
import commands
import time



pool = redis.ConnectionPool(host="47.93.137.206", port=20002, password="91eb221c")
r = redis.StrictRedis(connection_pool=pool)
pub = r.pubsub()
pub.subscribe('ci')
for item in pub.listen():
    if item['type'] == 'message':
        print "*******接受************" + '\n'
        data = item['data']
        print data
        # dev/beta/gray  [0-9]
        # sh 1.sh $env $flag $domain (haba , maijia , maijia)
        # domain.cfg < vyohui.com  bravetime.net  

        time.sleep(3)
        status, output = commands.getstatusoutput("cd /Users/dabenchen/Documents/davdian_python/test_api_dvd && \
        nosetests test_case/test_case_01_login_loginout.py test_case/test_case_02_login_getPageFirst_loginout.py test_case/test_case_03_login_getChannel_loginout.py test_case/test_case_04_login_getSearch_loginout.py test_case/test_case_05_login_timeShop_goodsDetail_loginout.py test_case/test_case_06_login_firstGuess_goodsDetail_loginout.py test_case/test_case_07_login_channel_goodsDetail_loginout.py test_case/test_case_08_login_channelGuess_goodsDetail_loginout.py test_case/test_case_09_login_groupList_goodsDetail_loginout.py test_case/test_case_10_login_firstBanner_loginout.py test_case/test_case_11_login_getPageFirst_timeShop_goodsDetail_addCart_loginout.py test_case/test_case_12_login_firstGuess_goodDetail_addCart_loginout.py test_case/test_case_13_login_getSearch_goodsDetail_addCart_loginout.py --with-html --html-report=nosetest_report/test_Report.html --html-report-template=/Library/Python/2.7/site-packages/nose_html_reporting/templates/report2.jinja2")
        print output
        print status
        

    elif item['data'] == 'over':
        break;
        
p.unsubscribe('ci')
print '取消订阅'

