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
'''

