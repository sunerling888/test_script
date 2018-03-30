#!/usr/bin/env python
# coding: utf-8

import hashlib
import urllib, urllib2
import json

class DavdianSession:
    ''' davdian 会话'''

    session = ''
    shopUrl = 'http://bravetime.davdian.com'      # 线上环境
    # shopUrl = 'https://' + yaya000 + domain['']
    # haba + domain.cfg (content)
    opener =  urllib2.build_opener()

    def __init__(self, mobile = None, password = None):
        if mobile and password:
            self._login(mobile, password)
        pass


    def api(self, uri, params = {}):
        requestParams = self._buildParams(params)
        sign = self._sign(requestParams)
        requestParams['sign'] = sign

        data = urllib.urlencode(requestParams)
        response = self.post(uri, data)
        if response['code'] != 200:
            return False

        j = json.loads(response['body'])

        session = j['sess_key']
        shopUrl = j['shop_url']
        print "DEBUG\t[%s][%s]" % (session, shopUrl)

        if session != self.session:
            self.opener = urllib2.build_opener()
            self.opener.addheaders.append(('Cookie','dvdsid=%s' % session))
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
            response = self.opener.open(url, data, timeout=1)
        except:
            print "ERROR"
            return {'code':-1, 'msg':'12345', 'body':''}

        if not response:
            #print "DEBUG\t[%s][%s][%s]" % (0, "", "")
            return {'code':0, 'msg':'', 'body':''}
        
        code = response.getcode()
        msg = response.msg
        data = response.read()

        #print "DEBUG\t[%s][%s][%s]" % (code, msg, data)
        return {'code':code, 'msg': msg, 'body': data}



if __name__ == '__main__':
    #session = DavdianSession('6f005e9fcbb77bfe032470ce401dccf401be6a43')
    session = DavdianSession('18600967174', 'aaaaaa')
    response = session.get('/settings.html')
    print response['body']
