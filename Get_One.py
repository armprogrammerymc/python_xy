#coding=utf-8
import argparse
import re
from multiprocessing import Pool
import requests
import bs4
import time
import json
import io
import os
import codecs

root_url = 'http://wufazhuce.com'

def get_url(num):
    return root_url + '/one/' + str(num)

def get_urls(num):
    #map加工
    urls = map(get_url, range(100,100+num))
    return urls

def get_data(url):
  dataList = {}
  response = requests.get(url)
  if response.status_code != 200:
      return {'noValue': 'noValue'}
  soup = bs4.BeautifulSoup(response.text,"html.parser")
  dataList["index"] = soup.title.string[4:7]
  for meta in soup.select('meta'):
    if meta.get('name') == 'description':
      dataList["content"] = meta.get('content')
  dataList["imgUrl"] = soup.find_all('img')[1]['src']
  return dataList

def download_img(imgUrl, i):
    img = requests.get(imgUrl,stream=True)
    img_name = "one" + str(i) + ".jpg"
    #get current work director
    base_dir = os.getcwd() + "/picture"
    with open(os.path.join(base_dir,img_name),'ab') as img_file:
      for chunk in img.iter_content(chunk_size=1024):
        if chunk:
          img_file.write(chunk)
          img_file.flush()
      img_file.close()

if __name__=='__main__':
###############################################
#爬虫主要需要4个步骤：
#1.发送一个需要爬取图片的url
#2.解析并获取需要的div
#3.找到你需要的图片的url
#4.下载图片并保存到本地
###############################################
#多线程：4个线程
  pool = Pool(4)
  dataList = []

  urls = get_urls(10)
  #获取当前时间
  start = time.time()
  #map加工list
  dataList = pool.map(get_data, urls)
  print "ymc: " + dataList[1]["imgUrl"]
  print "ymc: " + dataList[1]["index"]
  print "ymc: " + dataList[1]["content"]
 # download_img(dataList[1]["imgUrl"])
  for i in range(len(dataList)):
      download_img(dataList[i]["imgUrl"],i)
  end = time.time()
  print 'use: %.2f s' % (end - start)
  # 转存
  jsonData = json.dumps({'data':dataList},ensure_ascii=False,indent=2)
  print "ymc: " + jsonData
  #文件io操作
  with codecs.open('data.txt', 'w', 'utf-8') as outfile:
    json.dump(jsonData, outfile, ensure_ascii=False)
