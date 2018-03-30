            
        
        # 取出feedList
        feedList = data['data']['feedList']   
        # 设置长度
        length = len(feedList)

        # 最后包含了，所以要length - 1
        randIndex = random.randint(0, length - 1)
        
        # 随机取goodsid,还包含了一层['body']['dataList']
        goodsidIndex = random.randint(0, len(feedList[randIndex]['body']['dataList']) - 1)
        print feedList[randIndex]
        # 给定一个goodsId,判断，因为feedList里前几个没有goodsId
        goodsId = 0
        if feedList[randIndex]['body']['dataList'][goodsidIndex].has_key('goodsId'):
            goodsId = feedList[randIndex]['body']['dataList'][goodsidIndex]['goodsId']

        # 取出goodsid
        # goodsId = int(data['data']['feedList'][]['body']['dataList']['goodsId'])
        print goodsId
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)



        a = 123
        b = int(123)
        print a
        print b
        