#!/usr/bin/env python
# coding: utf-8
'''
vyohui.cn需要loaduser和randuser
'''

import hashlib
import urllib, urllib2
import json
import commands

class DavdianSession:
    ''' davdian 会话'''

    session = ''
    shopUrl = 'http://bravetime.davdian.com'
    # shopUrl = 'https://' + yaya000 + domain['']
    # haba + domain.cfg (content)
    opener =  urllib2.build_opener()

    def __init__(self, mobile = None, password = None):
        if mobile and password:
            self._login(mobile, password)
        # self.loadUser()
        # self.randUser()
        self._initOpener()
        pass
    '''
    def loadUser(self):
        # 文件路径
        with open("/home/xiaoqiang.li/scripts/release_li/domain.conf", "rb") as fd:
            reader = csv.reader(fd)
            print reader
            for arr in reader:
                self.user.append({'domain':arr[0]})

    def randUser(self):
        self.loadUser()
        user = self.user[0]
    '''

    def api(self, uri, params = {}):
        requestParams = self._buildParams(params)
        sign = self._sign(requestParams)
        requestParams['sign'] = sign

        data = urllib.urlencode(requestParams)
        response = self.post(uri, data)
        if response['code'] != 200:
            print "ERROR\t%s%s" % (uri, response['code'])
            return {'code': 0 - response['code'], 'message': 'http request error', 'data':None}
            # return False

        j = json.loads(response['body'])

        session = j['sess_key']
        shopUrl = j['shop_url']
        print "DEBUG\t[%s][%s]" % (session, shopUrl)

        if session != self.session:
            self.opener = urllib2.build_opener()
            self.opener.addheaders.append(('Cookie','dvdsid=%s' % session))
            self._initOpener()
            self.session = session
        self.shopUrl = shopUrl

        return j

    def get(self, uri):
        return self._request(uri, None)

    def post(self, uri, data = ''):
        if not data:
            data = ''
        return self._request(uri, data)

    def _login(self, mobile, password):
        response = self.api('/api/mg/auth/user/login', {'mobile':mobile, 'password':password})
        if not response or (int)(response['code']) != 0:
            return False
        return True

    def _buildParams(self, params):
        data = {
            'data_version': '0',
            'device_token': '',
            'format': 'json',
            'osv': 'web_h5_*_*',
            'sess_key': self.session,
            'shop_url': self.shopUrl,
            'ts': '1511242550937',
            'wh': '750_1334'
        }
        for key, value in params.items():
            data[key] = value
        return data

    def _sign(self, params):
        items = params.items()
        items.sort()
        data = ''.join(["%s=%s" % (k, v) for k, v in items])
        sign = hashlib.md5(data)
        return sign.hexdigest().upper()

    def _request(self, uri, data = None):
        url = self.shopUrl + uri
        print "DEBUG\t[%s][%s]" % (url, data)

        try:
            response = self.opener.open(url, data, timeout=20)
            '''     # 调试
            host_flag = ['18600960001', '18600960002', 'dabentest']
            for m in host_flag:
                status, output = commands.getstatusoutput("curl  http://"+m+".vyohui.cn/api/mg/auth/user/login -I -X POST")
                print output
            '''
        except Exception, e:
            # repr (e)
            print e
            #print url
            #print data
            print "ERROR"
            return {'code': 999999, 'msg': 'Request Exception', 'body': 'Request Exception'}

        if not response:
            #print "DEBUG\t[%s][%s][%s]" % (0, "", "")
            return {'code': 999999, 'msg': 'Request no response', 'body': 'Request no response'}
        
        code = response.getcode()
        msg = response.msg
        data = response.read()

        #print "DEBUG\t[%s][%s][%s]" % (code, msg, data)
        return {'code':code, 'msg': msg, 'body': data}

    def _initOpener(self):
        self.opener.addheaders = [item for item in self.opener.addheaders if item[0] != 'User-agent']
        self.opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'))



if __name__ == '__main__':
    #session = DavdianSession('6f005e9fcbb77bfe032470ce401dccf401be6a43')
    session = DavdianSession('18600967174', 'aaaaaa')
    response = session.get('/settings.html')
    print response['body']
