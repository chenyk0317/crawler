# -*- coding: utf-8 -*-

import re
import urllib
import urllib2
import os
import socket
import sys
import time

baseurl = 'http://cl.c1oulske1.pw/'
def getHtml(url):
    time.sleep(3)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
    req.add_header('Content-Type','text/html')
    try:
        res = urllib2.urlopen(req,timeout=10)
        html = res.read()
        htmlUnicode = html.decode('GBK');
        return htmlUnicode;
    #htmlUnicode = html.decode("GB18030");
    except Exception,e:
        print str(e)
        print url
        return ''
    return ''

def getUrlList(html):
    reg = r'<h3>(<a href="htm.+?)</h3>'
    name  =  re.compile(reg)
    namelist = re.findall(name,html)
    arr = []
    for item in namelist:
        #print item
        urlreg = r'(htm_data.+?\.html)'
        url = (re.search(urlreg,item)).group(0)
        url = baseurl + url
        arr.append(url)
    return arr

def getFinderName(html):
    findereg = r'<h4>(.+)</h4>'
    urllist = re.findall(re.compile(findereg),html)
    
    if urllist:
        finder = urllist[0]
        return finder
    return ''

def downloadImage(imageUrl,imageName):
    print imageUrl
    print imageName
    req = urllib2.Request(imageUrl)
    req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2526.106 Safari/537.36')
    try:
        path = imageName
        resp = urllib2.urlopen(req,timeout=60)
        respHtml = resp.read()
        binfile = open(path, "wb")
        binfile.write(respHtml)
        binfile.close()
        print '下载成功'
        print '................................'
    except Exception,e:
        print str(e)
        print '下载失败'
        print '................................'


def getImageUrlList(url):
    print '*********************************'
    html = getHtml(url)
    imagePath = './image/'
    isImagePathExists = os.path.exists(imagePath)
    if not isImagePathExists:
        os.mkdir(imagePath)
    namefinder = getFinderName(html)
    print namefinder
    print url
    print '=================================='
    path = imagePath + namefinder
    if  not os.path.exists(path):
        os.mkdir(path)
    reg = r'<div class="tpc_content do_not_catch">.*<input.+</div>'
    if not re.search(reg,html) is None:
        html = (re.search(reg,html)).group(0)
        urlreg = r'https?://[^?&<>。、]*?.jpg'
        urllist = re.findall(re.compile(urlreg),html)
        for url in urllist:
            imageNameReg = r'[^/]*?.jpg'
            imageName = (re.findall(re.compile(imageNameReg),url))[0]
            imagePath = path + '/' + imageName
            ispathExists = os.path.exists(imagePath)
            if  not ispathExists:
                downloadImage(url,imagePath)
    print '-----------------------------------'

def traverse(html):
    list = getUrlList(html)
    for item in list:
        getImageUrlList(item)

traverse(getHtml(baseurl+'thread0806.php?fid=16'))
#getImageUrlList('http://cl.c1oulske1.pw/htm_data/16/1508/1603662.html')


