#coding=utf-8
#url:http://weibo.com/tangocartoon?refer_flag=1005055013_&is_all=1
#class = WB_feed_detail clearfix
import bs4
import requests

tango_url = 'http://weibo.com/tangocartoon?refer_flag=1005055013_&is_all=1'
class_name = 'WB_feed_detail clearfix'
#1
def set_tango_url():
    return tango_url
#2
def parse_div(url):
    response = requests.get(url)
    print response.text
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    div = soup.select('class')
    print len(div)
    div1 = div[0].get(class_name)
    print div1
#3
def find_pic_url():
    pass
#4
def download_pic():
    pass


if __name__=='__main__':
    #1.send a url
    url = set_tango_url()

    #2.parse and spider div
    parse_div(url)
    #3.find picture's url

    #4.download picture
