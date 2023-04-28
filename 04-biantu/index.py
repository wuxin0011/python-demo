import os
import requests
from threading import Thread
from time import sleep, time
from random import choice, random as randomNumber
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# 创建文件夹
def create_path():
    path = os.getcwd() + "\\彼岸图"
    if not os.path.exists(path):
        os.mkdir(path)
    return path


# 提取解析之后的response数据
def parse_data(link):
    try:
        sleep(randomNumber() * 3)  # 添加休眠时间，防止访问服务器被封
        data = requests.get(url=link, headers=random_headers()).content.decode("gbk")
        html = BeautifulSoup(data, 'lxml')
        return html
    except:
        pass


# 提取数据
def get_imgList(data):
    # 获取图片链接地址
    img_list = data.find('div', {'class': 'slist'}, 'li').find_all("a")
    for i, img in enumerate(img_list):
        try:
            # 大图片的地址url
            if img.get("href") is not None:
                img_url = root_url + img.get("href")
                # 访问大图片地址
                jgp_html_data = parse_data(img_url)
                # 获取jpg格式的链接地址
                j_ = jgp_html_data.find("img").get("src")
                # 当获取不到url时不参与执行
                if j_ is not None:
                    jpg_url = root_url + j_
                    jpg_name = jgp_html_data.find('img').get('title')
                    # 多线程下载图片
                    if jpg_name is not None:
                        t1 = Thread(target=save, args=(jpg_url, jpg_name))
                        t1.start()
                    else:
                        jpg_name = jpg_url.split('/')[-1]
                        t1 = Thread(target=save, args=(jpg_url, jpg_name))
                        t1.start()

        except:
            print("下载失败")


# 保存图片
def save(jpg_url, jpg_name):
    # print("jpg_url:",jpg_url,"jpg_name:",jpg_name)
    jpg = requests.get(jpg_url, headers=random_headers()).content
    path = create_path()
    with open("{}//{}.jpg".format(path, jpg_name), "wb") as f:
        print("正在下载:", jpg_name)
        f.write(jpg)


# 保存图片
def save_tupian(link):
    # print("保存图片link：",link)
    # 访问大图片地址
    jgp_html_data = parse_data(link)
    # 获取jpg格式的链接地址
    jpg_url = root_url + jgp_html_data.find("img").get("src")
    # 图片name
    jpg_name = jgp_html_data.find('img').get('title')
    # 当title为none时候
    if jpg_name is not None:
        save(jpg_url, jpg_name)
    else:
        jpg_name = jpg_url.split('/')[-1]
        save(jpg_url, jpg_name)


def run(href, printPage):
    for n in range(1, printPage + 1):
        try:
            print("======================正在下载第{}页数据=======================".format(n))
            html_data = parse_data(href)
            get_imgList(html_data)
            # 下一页链接地址
            next_link_page = html_data.find("div", {"class": "page"})
            for i in next_link_page:
                if i.get_text() == "下一页":
                    url = root_url + i.get("href")
                    href = url
        except Exception as e:
            print(e)
            print("爬取失败！")


def start():
    while True:
        try:
            link = input("下载的链接页的起始页链接仅支持\nhttp://pic.netbian.com的图片：")
            s_url = link.split("/")
            if "http:" in s_url or 'https:' in s_url:  # 判断是不是下载链接地址
                # if 'pic:' in s_url:  # 判断是不是下载链接地址
                print("保存地址：", create_path())
                if "tupian" in s_url:  # 判断图片链接是否是最终链接地址
                    save_tupian(link)
                    break
                else:
                    num = int(input("请输入要下载的页码数："))
                    if num >= 1:
                        run(link, num)
                        break
                    else:
                        print("下载页码必须大于等于1！")
                        continue
            else:
                continue
        except Exception as e:
            print(e)
            continue


# 创建随机请求头函数
def random_headers():
    # """通过列表的形式随机取得一个请求头，防止报错"""
    try:
        return {"User-Agent": UserAgent(verify_ssl=False).random}
    except:
        return {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48'
        }


if __name__ == '__main__':
    # 拼接链接的地址
    root_url = "http://pic.netbian.com/"
    example_urls = [
        'https://pic.netbian.com/4kmeinv/',
        'https://pic.netbian.com/4kfengjing/',
        'https://pic.netbian.com/tupian/27978.html',
        'https://pic.netbian.com/4kdongman/'
    ]
    print("例如")
    for i in example_urls:
        print(i)
    # print(headers)
    while True:
        s_time = time()
        start()
        e_time = time()
        print("花费时间：", str(int(e_time - s_time)) + "s")
        answer = input("是否继续y?")
        if answer == 'y' or answer == "Y":
            continue
        else:
            break
