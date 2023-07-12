import random
import re
from os import getcwd as os_getcwd, path as os_path, makedirs as os_makedirs
from random import random as randomNumber
from threading import Thread
from time import sleep, time

from bs4 import BeautifulSoup
from requests import get as req_get

picture_type = {
    'new': '最新',
    '4kfengjing': '风景',
    '4kmeinv': '美女',
    '4kdongman': '动漫',
    '4kyouxi': '游戏',
    '4kyingshi': '影视',
    '4kqiche': '汽车',
    '4kdongwu': '动物',
    '4krenwu': '人物',
    '4kzongjiao': '宗教',
    'shoujibizhi': '手机壁纸',
    'pingban': '平板壁纸',
    'tupian': '图片',
    's/4kyuanchuang': '原创',
}

list_useragent = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 "
    "Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
    "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14"
]


# 创建随机请求头函数
def random_headers():
    return {
        'user-agent': random.choice(list_useragent)
    }


# 创建文件夹
def create_path():
    path = os_getcwd() + f"\\彼岸图\\{link_type}"
    if not os_path.exists(path):
        os_makedirs(path)
    return path


# max_sleep_times = 0

# 提取解析之后的response数据
def response_html(link):
    html = None
    web_encoding = None
    try:
        sleep(randomNumber() * max_sleep_time)  # 添加休眠时间，防止访问服务器被封
        data = req_get(url=link, headers=random_headers(), verify=True)
        if data.status_code == 200:
            if is_pic_netbian_top(link):
                text = data.content.decode("utf-8")
            elif is_pic_netbian_com(link):
                text = data.content.decode("gbk")
            html = BeautifulSoup(text, 'html.parser')
        else:
            print("响应失败！")
        return html
    except Exception as e:
        print("响应失败！{}", e)
        return None


# 提取数据
def get_imgList(data):
    # 获取图片链接地址
    img_list = data.find('div', {'class': 'slist'}, 'li').find_all("a")
    for i, img in enumerate(img_list):
        try:
            # 大图片的地址url
            if img.get("href") is not None:
                img_url = check_url(f'{root_url}{img.get("href")}')
                # 访问大图片地址
                result = get_img_url_and_name(img_url)
                save(result['url'], result['name'])

        except:
            print("下载失败")


# 保存图片
def save(jpg_url, jpg_name):
    if jpg_url is not None:
        if jpg_name is None or jpg_name == '':
            jpg_name = f'{time()}'
        jpg = req_get(jpg_url, headers=random_headers()).content
        path = create_path()
        with open("{}//{}.jpg".format(path, jpg_name), "wb") as f:
            f.write(jpg)
        print("下载成功！{}".format(jpg_name))


def check_url(url: str) -> str:
    tcp = ''
    if url.startswith("https://"):
        tcp = 'https://'
    elif url.startswith("http://"):
        tcp = "http://"
    return f'{tcp}{url.replace(tcp, "").replace("///", "/").replace("//", "/")}'


def get_img_url_and_name(link):
    result = {
        'url': None,
        'name': None
    }
    jgp_html_data = response_html(link)
    if jgp_html_data is None:
        return result
    # 获取jpg格式的链接地址
    img = jgp_html_data.select_one("div.photo-pic a#img img")
    if img is None:
        return result
    result['url'] = img.get('src')
    result['name'] = img.get('alt')
    if result['name'] == '' or result['name'] is None:
        result['name'] = img.get('data-pic').split('/')[-1]
    return result


# 保存图片
def save_tupian(link):
    result = get_img_url_and_name(link)
    save(result['url'], result['name'])


def run(href, printPage):
    link_type = parse_link_type(href)
    print("下载类型为 【", link_type, "】 下载地址为:", href, "共计:", printPage, '页')
    print("保存地址：", create_path())
    for n in range(1, printPage + 1):
        try:
            print("======================正在下载第{}页数据=======================".format(n))
            html_data = response_html(href)
            if html_data is None:
                print("======================下载第{}页数据失败=======================".format(n))
                break
            get_imgList(html_data)
            # 下一页链接地址
            next_link_page = html_data.find("div", {"class": "page"})
            for i in next_link_page:
                if i.get_text() == "下一页":
                    url = root_url + i.get("href")
                    href = url
        except Exception as e:
            print("爬取失败！{} {}".format(n, e))


def is_pic_netbian_com(url) -> bool:
    return re.match(r'^(https|http)://.*\.netbian\.com\.*', url, re.I) is not None


def is_pic_netbian_top(url) -> bool:
    return re.match(r'^(https|http)://.*\.netbian\.top\.*', url, re.I) is not None


def is_support(url):
    return re.match(r'^(https|http)://.*\.netbian.*', url, re.I) is not None


def is_picture_url(url):
    return re.match(r'^(https|http)://.*\.netbian\..*/tupian/\d+\.html', url, re.I) is not None


def parse_link_type(input_url):
    for k, v in picture_type.items():
        url = r'https://.*\.netbian\..*/' + k + r'(.*)'
        if re.match(url, input_url, re.I):
            return v
    return "默认"


def menu_sleep_time():
    try:
        max_sleep_time = int(
            input('单个链接最大休眠时间【防止被网站封禁 默认最大为 2s】 输入 0-5 之间数字 超过5 将设置为5:'))
        if max_sleep_time < 0:
            max_sleep_time = 0
        elif max_sleep_time > 5:
            max_sleep_time = 5
    except:
        max_sleep_time = 2
    print(f"最大休眠时间为:{max_sleep_time}s")


def start():
    while True:
        try:
            menu()
            link = input("请输入地址或者输入序号 1-14:")
            if re.match(r'\d+', link):
                num = input("请输入总共要下载的页码数 默认为 1 页 ：")
                if num == '':
                    num = '1'
                if re.match(r'\d+', num):
                    if int(num) >= 1:
                        menu_sleep_time()
                        run(example_urls[int(link) - 1], int(num))
                        break
                    else:
                        print("下载页码必须大于等于1！")
                        continue
                else:
                    print("请输入数字")
                    continue

            if is_support(link):  # 判断是不是下载链接地址
                if is_picture_url(link):  # 判断图片链接是否是最终链接地址
                    save_tupian(check_url(f'{link}'))
                    break
                else:

                    num = input("请输入要下载的页码数：")
                    if re.match(r'\d+', num):
                        if int(num) >= 1:
                            menu_sleep_time()
                            run(link, int(num))
                            break
                        else:
                            print("下载页码必须大于等于1！")
                            continue
                    else:
                        print("请输入数字")
                        continue
            else:
                continue
        except Exception as e:
            print(e)
            continue


def menu():
    global max_sleep_time
    global link_type
    #  判断链接类型
    link_type = '默认'
    max_sleep_time = 2
    index = 1
    print("\n==============================默认菜单====================")
    for k, v in picture_type.items():
        print('序号', index, '类型', v, "下载地址:", f'{root_url}{k}')
        index = index + 1
    print("==========================================================")
    print("下载的链接页的起始页链接仅支持https://pic.netbian.com的图片：")


def input_root_url():
    global root_url
    print(" 1 https://pic.netbian.com/ （默认）")
    print(" 2 https://pic.netbian.top/ ")
    try:
        url = int(input("请选择链接源 默认为 1"))
        if url != '2':
            root_url = 'https://pic.netbian.top/'
        else:
            root_url = 'https://pic.netbian.com/'
    except:
        root_url = 'https://pic.netbian.com/'
    print(f"使用下载源为 {'https://pic.netbian.com/'}")


def start_select_input():
    input_root_url()
    global example_urls
    example_urls = []
    for k in picture_type.keys():
        example_urls.append(f'{root_url}{k}/')
    while True:
        s_time = time()
        start()
        e_time = time()
        print("\n本次下载花费时间 {} s".format(int(e_time - s_time)))
        answer = input("是否继续y?")
        if answer == 'y' or answer == "Y":
            continue
        else:
            print("\n 拜拜! \n")
            break


if __name__ == '__main__':
    start_select_input()
