#!/usr/bin/env Python
# -*- coding:utf-8 -*-

__author__ = 'daben_chen'

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
import time


# =====邮箱配置======

host_server = 'smtp.qiye.163.com'   #企业邮箱服务器
send_mail = 'chendaben@davdian.com'
pwd = 'Love112728'
send_mail = 'chendaben@davdian.com'
# receiver = ['chendaben@davdian.com']
receiver = ['davtest@davdian.com']
# receiver_CC = ['jiangmingzhu@davdian.com', 'songlirong@davdian.com', 'sunerling@davdian.com', 'duxue@davdian.com']


# 邮件的正文内容
# mail_content = "Dear all: <p>以下接口测试结果:<p><br>/api/mg/auth/user/login<p><p><br>/api/mg/auth/user/logout</p><br><p>请查收！</p>"
mail_content = "Hi: <p>以下4个流程 测试结果:<p><br>01.登录 -> 输入手机号、密码 -> 个人中心 -> 设置页面 -> 退出登录 [卖家/买家/游客] \
<br>02.登录 -> 首页（第一屏、搜索、菜单、猜你喜欢） -> 退出登录 [卖家/买家/游客]\
<br>03.登录 -> 首页（第一屏、猜你喜欢） -> 搜索(建议词、热词、搜索结果) -> 退出登录 [卖家/买家/游客]\
<br>04.登录 -> 首页（第一屏、猜你喜欢） -> 二级菜单(第一屏、猜你喜欢) -> 退出登录 [卖家/买家/游客] \
<p> 请查收!</p>"
# 邮件标题
mail_title = '接口测试报告'

# 邮件正文内容
msg = MIMEMultipart()
msg['Subject'] = Header(mail_title, 'utf-8')
msg['Form'] = send_mail
# msg['To'] = Header('chendaben@davdian.com', 'utf-8')
msg['To'] = '. '.join(receiver)
# msg['CC'] = '. '.join(receiver_CC)

msg.attach(MIMEText(mail_content, 'html', 'utf-8'))


# 构造附件1，传送当前目录下的nosetests.html文件
att1 = MIMEText(open('/Users/dabenchen/Documents/davdian_python/test_api_dvd/nosetest_report/test_report_20180322.html', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="test_report_20180322.html"'
msg.attach(att1)


# ssl登录
smtp = SMTP_SSL(host_server)
#set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
# smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(send_mail, pwd)

# smtp.sendmail(send_mail, receiver + receiver_CC,msg.as_string())
smtp.sendmail(send_mail, receiver, msg.as_string())
smtp.quit()