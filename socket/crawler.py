#!/usr/bin/env python
# coding=utf-8

import re
import urllib2
import threading
import json
import jieba
from time import sleep
from lxml import etree
from selenium import webdriver
from pymongo import MongoClient

topK = 2

taobao_goods = []
tmall_goods = []
jingdong_goods = []

def tmall_list(url, price, headers):
    try:
        request = urllib2.Request(url=url, headers=headers)
        res = urllib2.urlopen(request).read()
        tree = etree.HTML(res)
    except Exception, e:
        print 'Error: %s' % e

    title = tree.xpath('//div[@class="tb-detail-hd"]/h1/text()')[0].encode('utf-8').strip()
    shop = tree.xpath('//a[@class="slogo-shopname"]/strong/text()')[0].encode('utf-8').strip()
    shop_url = 'https:' + tree.xpath('//a[@class="slogo-shopname"]/@href')[0]
    describeScore = tree.xpath('//div[@id="shop-info"]/div[2]/div[1]/div[2]/span/text()')[0]
    serviceScore = tree.xpath('//div[@id="shop-info"]/div[2]/div[2]/div[2]/span/text()')[0]
    logisticsScore = tree.xpath('//div[@id="shop-info"]/div[2]/div[3]/div[2]/span/text()')[0]
    
    tmall_goods.append(url)
    tmall_goods.append(unicode(title))
    tmall_goods.append(price)
    tmall_goods.append(unicode(shop))
    tmall_goods.append(shop_url)
    tmall_goods.append(str((float(describeScore)+float(serviceScore)+float(logisticsScore))/3)[:3])

def jingdong_list(url):
    try:
        res = urllib2.urlopen(url).read().decode('GBK', 'ignore')
        tree = etree.HTML(res)
    except Exception, e:
        print "Error: %s" % e
    title = tree.xpath('//div[@class="sku-name"]/text()')[0].encode('utf-8').strip()
    shop = tree.xpath('//div[@class="name"]/a/text()')[0].encode('utf-8').strip()
    shop_url = 'https:' + tree.xpath('//div[@class="name"]/a/@href')[0]
    try:
        compositeScore = tree.xpath('//em[@class="evaluate-grade"]/span/a/text()')[0]
    except Exception, e:
        compositeScore = ''

    data = url.split('/')
    skuids = data[3][:-5]
    purl = 'https://p.3.cn/prices/mgets?skuIds=J_' + skuids
    pricedata = urllib2.urlopen(purl).read()
    jdata = json.loads(pricedata)
    price = jdata[0]["p"]

    jingdong_goods.append(url)
    jingdong_goods.append(unicode(title))
    jingdong_goods.append(price)
    jingdong_goods.append(unicode(shop))
    jingdong_goods.append(shop_url)
    jingdong_goods.append(compositeScore)

def taobao_list(thisid, headers):
    gurl = "https://item.taobao.com/item.htm?id=" + str(thisid)
    try:
        request = urllib2.Request(url=gurl, headers=headers)
        res = urllib2.urlopen(request).read().decode('gb2312', 'ignore')
        tree = etree.HTML(res)
    except Exception, e:
        print 'Error: %s' % e

    title = tree.xpath('//h3[@class="tb-main-title"]/text()|//h3[@class="tb-main-title"]/@data-title')[0].strip().strip('\r\n').encode('utf-8')
    #price = tree.xpath('//em[@class="tb-rmb-num"]/text()')[0]
    url = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId={}&modules=price,xmpPromotion".format(thisid)
    req = urllib2.Request(url=url, headers=headers)
    res = urllib2.urlopen(req).read()
    data = list(set(re.findall('"price":"(.*?)"', res)))
    price = ""
    for t in data:
        if '-' in t:
            price = t
            break
    if not price:
        price = sorted(map(float, data))[0]
    #print price
    try:
        shop = tree.xpath('//div[@id="J_ShopInfo"]//dl/dd/strong/a/text()')[0].strip()
        shop_url = "http:" + tree.xpath('//*[@id="J_ShopInfo"]//dl/dd/strong/a/@href')[0]
    except Exception, e:
        shop = u"淘宝店铺"
        shop_url = u"https://www.taobao.com/"
    try:
        describeScore = tree.xpath('//div[@class="tb-shop-rate"]/dl[1]/dd/a/text()')[0].strip()
        serviceScore = tree.xpath('//div[@class="tb-shop-rate"]/dl[2]/dd/a/text()')[0].strip()
        logisticsScore = tree.xpath('//div[@class="tb-shop-rate"]/dl[3]/dd/a/text()')[0].strip()
    except Exception, e:
        describeScore = '0'
        serviceScore = '0'
        logisticsScore = '0'

    taobao_goods.append(gurl)
    taobao_goods.append(unicode(title))
    taobao_goods.append(price)
    taobao_goods.append(shop)
    taobao_goods.append(shop_url)
    taobao_goods.append(str((float(describeScore)+float(serviceScore)+float(logisticsScore))/3)[:3])

class Crawler:
    def __init__(self, url=None):
        self.client = MongoClient('localhost', 27017)
        mdb = self.client['test']
        self.collection = mdb['test']

        self.url = url
        self.data = self.url.split('/')
        self.headers = {
            'Accept':'application/json, text/plain, */*',
            'Accept-Language':'zh-CN,zh;q=0.3',
            'referer': 'https://item.taobao.com/item.htm?id=543224175019',
            'cookie': 'thw=cn; miid=1877326715353705246; ctoken=0P0JvKEIyk15qEwpK8LIiceland; tk_trace=oTRxOWSBNwn9dPyscxqAz9fIO73QQFhF7kVkgTL59JVC7kpGpQEdOb67caDmPjbIYxYMRUFXKcCXX%2FfQ1h8gXuGVrgjD61F%2B0DFnRC5EMB7aZ9NOo63GAUmnCjjrIY5wkGyucBWS44YHI4A6d%2BLNSACICaG8KC2tFYpVmX%2BjxKj4tEcAteNhxHEPvOhSJbYqgm9OvDy9VPmorkl1GZEBZo8OvIgVoPbrrTrCdOyH18y6BkHGva4kbB8xuQw62sSLb2eyt8bjx62%2B1sUCi8z0z2oWb26s6hziPr0T5GVnMnPDD%2Bmuyr6pAHiyPPI4OKTerpb3ea5uGXy8TcrjbxvIiQldLj5pLEUsZu8%3D; UM_distinctid=15e22e6bc6e1-0c5735b42741ab-3976045e-100200-15e22e6bc6f435; _m_h5_tk=8c383678bc2922e1521fbd203debdbaf_1503827636199; _m_h5_tk_enc=df906285a00b4f52fbc6c9fe8d3bc421; hng=CN%7Czh-CN%7CCNY%7C156; v=0; uss=BqeJtzLVJrTsSJ6X2LDYRdaWQ%2BKUXOOY8l7NE73sSoPSShTwCqvcl%2FyDvA%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _tb_token_=533b3393509e0; whl=-1%260%260%261503930679329; cna=jiIfEsNey0MCAXUg2C6F55ir; uc1=cookie14=UoTcDNNnZUea6w%3D%3D&lng=zh_CN&cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&existShop=false&cookie21=V32FPkk%2Fgipm&tag=8&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&pas=0; uc3=sg2=VypZNAKKWWqEaSKA1GpGs%2B8tysrnwEF9TzJHu9Fo6tw%3D&nk2=F5RDKmmBskqoP%2BFa&id2=UU27LTb95wEmtQ%3D%3D&vt3=F8dBzWYdKC42Yr%2BbE1E%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; existShop=MTUwMzk3MzcwNg%3D%3D; lgc=tb6668866688; tracknick=tb6668866688; cookie2=1055c0500c661fa5398031aa3bd27f5c; sg=897; mt=np=&ci=115_1&cyk=2_0; cookie1=B0eg4Md2wVeUEGrrbnYlnTqeCodw3QYsxMUcV2cWzeY%3D; unb=2592924029; skt=c0e93da15ffb6fec; t=f24179ca58a99063c6f1feabcbc17b12; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=tb6668866688; cookie17=UU27LTb95wEmtQ%3D%3D; isg=Ai8v8hTwqgLcE64Dpfv1gA-vvkr5fJ1c2I7spUG8dB6lkE2SSaUrRjUAZLZV; linezing_session=QJXBwjEeb4zxNhS670MXjI85_1503973736042rHlv_10',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Connection':'keep-alive',
        }

        try:
            request = urllib2.Request(url=url, headers=self.headers)
            self.response = urllib2.urlopen(request).read()
            self.tree = etree.HTML(self.response)
        except Exception, e:
            return '链接输入有误!!!'

    def spider_taobao(self):
        item = []
        
        try:
            if self.data[3].startswith('?spm=a21bo.50862.201857'):
                return '1级'
            
            elif self.data[3] == 'markets':
                return '2级'
           
            elif self.data[3].startswith('list'):
                del taobao_goods[:]
                patid = '"nid":"(.*?)"'
                allid = re.findall(patid, self.response)
                item.append('hp')
                for thisid in allid:
                    t = threading.Thread(target=taobao_list, args=(thisid, self.headers))
                    t.start()
                
                sleep(3)
                item.extend(taobao_goods)

                return item

            elif self.data[3].startswith('item'):
                print '4级'
                title = self.tree.xpath('//h3[@class="tb-main-title"]/@data-title')[0]
                url = self.url
                price = self.tree.xpath('//em[@class="tb-rmb-num"]/text()')[0]
                shop = self.tree.xpath('//*[@id="J_ShopInfo"]//dl/dd/strong/a/text()')[0].strip()
                shop_url = "http:" + self.tree.xpath('//*[@id="J_ShopInfo"]//dl/dd/strong/a/@href')[0]
                try:
                    describeScore = self.tree.xpath('//div[@class="tb-shop-rate"]/dl[1]/dd/a/text()')[0].strip()
                    serviceScore = self.tree.xpath('//div[@class="tb-shop-rate"]/dl[2]/dd/a/text()')[0].strip()
                    logisticsScore = self.tree.xpath('//div[@class="tb-shop-rate"]/dl[3]/dd/a/text()')[0].strip()
                except Exception, e:
                    describeScore = ''
                    serviceScore = ''
                    logisticsScore = ''
                
                item.append('hp')
                item.append(str(url))
                item.append(title)
                item.append(price)
                item.append(shop)
                item.append(shop_url)
                item.append(str((float(describeScore)+float(serviceScore)+float(logisticsScore))/3)[:3])
                
                return item

            elif self.data[3].startswith('?spm=a21bo.50862.201867-main'):
                return '特殊级别!'
            else:
                return '敬请期待!!!'
        except Exception, e:
            print e
            if self.data[2].endswith('taobao.com'):
                return '1级'
            else:
                return '未知错误!!!'
    
    def spider_tmall(self):
        item = []
        print self.data
        try:
            if self.data[3].startswith('search'):
                del tmall_goods[:]
                item.append('hp')
                gurls = self.tree.xpath('//p[@class="productTitle"]/a/@href')
                prices = self.tree.xpath('//p[@class="productPrice"]/em/@title')
                
                num = len(gurls)

                for i in xrange(num):
                    gurl = "https:" + gurls[i]
                    t = threading.Thread(target=tmall_list, args=(gurl, prices[i], self.headers))
                    t.start()
                
                sleep(1.2)
                item.extend(tmall_goods)
                return item

            elif self.data[3].startswith('item'):
                print self.url
                
                headers = self.headers
                headers['referer'] = "https://detail.tmall.com/item.htm"
                itemId = re.findall('id=(.*?)&', self.url)[0]
                priceurl = "https://mdskip.taobao.com/core/initItemDetail.htm?&itemId=" + itemId
                
                req = urllib2.Request(url=priceurl, headers=headers)
                res = urllib2.urlopen(req).read()
                data = re.findall('"postageFree":false,"price":"(.*?)","promType"', res)
                price = list(set(data))[0]

                title = self.tree.xpath('//div[@class="tb-detail-hd"]/h1/text()')[0].encode('utf-8').strip()
                url = self.url
                shop = self.tree.xpath('//a[@class="slogo-shopname"]/strong/text()')[0].encode('utf-8').strip()
                shop_url = 'https:' + self.tree.xpath('//a[@class="slogo-shopname"]/@href')[0]
                describeScore = self.tree.xpath('//div[@id="shop-info"]/div[2]/div[1]/div[2]/span/text()')[0]
                serviceScore = self.tree.xpath('//div[@id="shop-info"]/div[2]/div[2]/div[2]/span/text()')[0]
                logisticsScore = self.tree.xpath('//div[@id="shop-info"]/div[2]/div[3]/div[2]/span/text()')[0]
                

                item.append('hp')
                item.append(str(url))
                item.append(unicode(title))
                item.append(price)
                item.append(unicode(shop))
                item.append(shop_url)
                item.append(str((float(describeScore)+float(serviceScore)+float(logisticsScore))/3)[:3])
                
                return item

        except Exception, e:
            pass
   
    def spider_jingdong(self):
        item = []
        print self.data
        try:
            if self.data[2].startswith('list'):
                del jingdong_goods[:]
                item.append('hp')
                urls = self.tree.xpath('//div[@id="plist"]/ul/li/div/div/div[2]/div[1]/div[3]/a/@href')
                
                for url in urls:
                    gurl = "https:" + url
                    t = threading.Thread(target=jingdong_list, args=(gurl,))
                    t.start()
            
                sleep(2)
                item.extend(jingdong_goods)

                return item

            elif self.data[2].startswith('search'):
                del jingdong_goods[:]
                item.append('hp')
                urls = self.tree.xpath('//div[@id="J_goodsList"]/ul/li/div/div/a/@href')
                
                for url in set(urls):
                    if url.startswith('//item'):
                        gurl = "https:" + url
                        print gurl
                        t = threading.Thread(target=jingdong_list, args=(gurl,))
                        t.start()
            
                sleep(2)
                item.extend(jingdong_goods)

                return item

            elif self.data[2].startswith('item'):
                print self.url
                #print self.response.decode("GBK", "ignore")

                title = self.tree.xpath('//div[@class="sku-name"]/text()')[0].encode('utf-8').strip()
                shop = self.tree.xpath('//div[@class="name"]/a/text()')[0].encode('utf-8').strip()
                shop_url = 'https:' + self.tree.xpath('//div[@class="name"]/a/@href')[0]
                try:
                    compositeScore = self.tree.xpath('//em[@class="evaluate-grade"]/span/a/text()')[0]
                except Exception, e:
                    compositeScore = ''
                
                data = self.url.split('?')[0].split('/')
                skuids = data[3][:-5]
                purl = 'https://p.3.cn/prices/mgets?skuIds=J_' + skuids
                pricedata = urllib2.urlopen(purl).read()
                jdata = json.loads(pricedata)
                price = jdata[0]["p"]

                print title
                print self.url
                print price
                print shop
                print shop_url
                print compositeScore

                item.append('hp')
                item.append(self.url)
                item.append(unicode(title))
                item.append(price)
                item.append(unicode(shop))
                item.append(shop_url)
                item.append(compositeScore)
        
                return item
        except Exception, e:
            pass

    def spider_sinablog(self):
        try:
            if self.data[3] == 's':
                title = self.tree.xpath('//*[@class="articalTitle"]/h2/text()')
                print title
                if not title:
                    title = self.tree.xpath('//div[@class="BNE_title"]/h1/text()')[0].encode('utf-8')
                    release_time = self.tree.xpath('//span[@id="pub_time"]/text()')[0]

                    tempdata = self.tree.xpath('//div[@class="tagbox"]/a/text()')
                    btags = "   ".join(tempdata).encode('utf-8')
                    print title
                    print release_time
                    print tempdata
                else:
                    pass
                article = ""
                data = self.tree.xpath('//*[@id="sina_keyword_ad_area2"]')
                for part in data:
                    article = part.xpath('string(.)').encode('utf-8')

                #tags = jieba.analyse.extract_tags(article,topK=topK)
                #keywords = (','.join(tags))
                
                item = "标题:  " + title.strip() + "\n\n发布时间:  " + release_time + "\n\n标签:  " + btags + "\n\n正文: \n\n" + article.rstrip('\r\n') + "\n\n"
            
            return item
        except Exception, e:
            print e
            return '未知错误!!!'
    
    def spider_csdnblog(self):
        try:
            if self.data[5] == 'details':
                title = self.tree.xpath('//span[@class="link_title"]/a/text()')
                if not title:
                    title = self.tree.xpath('//h1[@class="csdn_top"]/text()')[0].encode('utf-8')
                    release_time = self.tree.xpath('//span[@class="time"]/text()')[0].encode('utf-8')
                    readnum = self.tree.xpath('//button[@class="btn-noborder"]/span/text()')
                    tempdata = self.tree.xpath('//ul[@class="article_tags clearfix tracking-ad"]/li/a/text()')
                    btags = '   '.join(tempdata).encode('utf-8')
                    sort = self.tree.xpath('//div[@class="artical_tag"]/span[1]/text()')[0].encode('utf-8')
                else:
                    head = ""
                    for t in title:
                        head += t
                    title = head.encode('utf-8').strip('\r\n')
                    release_time = self.tree.xpath('//span[@class="link_postdate"]/text()')[0]
                    readnum = self.tree.xpath('//span[@class="link_view"]/text()')[0].encode('utf-8')[:-9]
                    tempdata = self.tree.xpath('//span[@class="link_categories"]/a/text()')
                    btags = '   '.join(tempdata).encode('utf-8')
                    print type(btags)
                    tdata = self.tree.xpath('//div[@class="bog_copyright"]/text()')
                    if not tdata:
                        sort = "转载"
                    else:
                        sort = "原创"

                    #sort = self.tree.xpath('//div[@class="category_r"]/label/span/text()')[0].encode('utf-8')
                article = ""
                data = self.tree.xpath('//*[@class="markdown_views"]')
                if not data:
                    data = self.tree.xpath('//div[@id="article_content"]')

                for part in data:
                    article += part.xpath('string(.)').encode('utf-8')
                article = article.lstrip('\r\n')
                

                item = "标题:  " + title.strip() + "\n\n发布时间:  " + release_time + "\n\n类别:  " + sort + "\n\n标签:  " + btags + "\n\n阅读人数:  " + readnum + "\n\n正文: \n\n" + article.rstrip('\r\n') + "\n\n"
                return item
        except Exception, e:
            print e
            return '未知错误!!!'

    def spider_sinanews(self):
        pass

    def spider_chinanews(self):
        pass
