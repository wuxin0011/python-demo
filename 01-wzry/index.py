'''
王者荣耀官方 英雄壁纸爬取
'''
import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import time
import random
import re


def get_fake_userAgent():
    try:
        return {
            'User-Agent':UserAgent().random
        }
    except:
         return {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50'
        }


def get_response(url):
    time.sleep(random.choice([1,2,3,4,5]))
    try:
        response = requests.get(url=url,headers=get_fake_userAgent())
        if response and response.status_code==200:
            return response.content
        else:
            return None
    except Exception as e:
        print(f"响应失败{url}",e)
        return None
    

def parse_single_hero_data(url):
    res = get_response(url).decode('gbk')
    # 获取英雄id
    hero_id = re.search(r'/\d+\.shtml',url,re.I)[0].replace('/','').replace('.shtml','')
    if res:
        soup = BeautifulSoup(res,'lxml')
        # 英雄名称
        hero_name = soup.select_one('div.cover h2.cover-name').get_text()
        hero_skin_name_list = soup.select('ul.pic-pf-list.pic-pf-list3')[0]['data-imgname']
        hero_skin_name_list = re.sub(r'(&\d+)','',hero_skin_name_list,re.M).split('|')
        # 皮肤遍历下载
        # 创建文件夹
        save_hero_skin(hero_id,hero_name,hero_skin_name_list)
   
       

def save_hero_skin(hero_id,hero_name,hero_skin_link_list):
    path = os.getcwd()+'\\img\\'+hero_name
    if not os.path.exists(path):
        os.makedirs(path)
    for i,skin_name in enumerate(hero_skin_link_list):
        try:
            link = skin_skin_link.format(hero_id,hero_id,i+1)
            content = get_response(link)
            if content:
                with open(f'{path}//{skin_name}.jpg',mode='wb') as file:
                    file.write(content)
            print(hero_name + skin_name ,'下载成功')
        except Exception as e:
            print(hero_name + skin_name ,'下载失败！',e)

        



def get_hero_list(url):
    data = get_response(url).decode('gbk')
    if data:
        soup = BeautifulSoup(data,'lxml')
        hero_link_list = soup.select('ul.herolist.clearfix li a')
        for index,hero_link in enumerate(hero_link_list):
            # 地址拼接替换
            hero_link_list[index] = root_url + hero_link['href']
        return hero_link_list
    else:
        return []




def start():
    # 执行初始地址
    hero_link_list = get_hero_list(init_url)
    # 遍历查找
    for link in hero_link_list:
        parse_single_hero_data(link)


if __name__ == '__main__':
    # 初始地址
    root_url = 'https://pvp.qq.com/web201605/'
    # 英雄列表地址
    init_url = 'https://pvp.qq.com/web201605/herolist.shtml'
    skin_skin_link = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'
    # 存放英雄地址
    hero_link_list = [ ]
    start()
    