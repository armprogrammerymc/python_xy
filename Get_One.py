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
    base_dir = os.getcwd() + "//"
    with open(os.path.join(base_dir,img_name),'wb') as img_file:
      for chunk in img.iter_content(chunk_size=1024):
        if chunk:
          img_file.write(chunk)
          img_file.flush()
      img_file.close()

if __name__=='__main__':
  pool = Pool(4)
  dataList = []
  urls = get_urls(10)
  start = time.time()
  dataList = pool.map(get_data, urls)
  print "liubei: " + dataList[1]["imgUrl"]
  print "liubei: " + dataList[1]["index"]
  print "liubei: " + dataList[1]["content"]
 # download_img(dataList[1]["imgUrl"])
  for i in range(len(dataList)):
      download_img(dataList[i]["imgUrl"],i)
  end = time.time()
  print 'use: %.2f s' % (end - start)
  jsonData = json.dumps({'data':dataList},ensure_ascii=False,indent=2)
  print "liubei: " + jsonData
  with codecs.open('data.txt', 'w', 'utf-8') as outfile:
    json.dump(jsonData, outfile, ensure_ascii=False)
