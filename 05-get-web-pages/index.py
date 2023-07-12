'''
获取网站全部内容
'''
import os
import random
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

file_ext = ['.html']  # 默认 后缀
is_get_file_ext = ['False']  # 是否是初始化了
# 需要下载html地址
html_url_list = []
# 需要下载 css 列表
css_url_list = []
# 需要下载js列表
js_url_list = []
# 需要下载图片地址
img_url_list = []
# 需要下载的字体
font_url_list = []
# 需要下载的audio
audio_url_list = []
# 需要下载的video
video_url_list = []
# 已经下载html地址
already_download_html_list = []
# 已经下载html地址
already_download_css_list = []
# 已经下载js地址
already_download_js_list = []
# 已经下载img地址
already_download_img_list = []
# 已经下载font地址
already_download_font_list = []
# 已经下载video地址
already_download_video_list = []
# 已经下载audio地址
already_download_audio_list = []

exclude = ['tel:', 'file:', 'data:', 'void(0)', 'javascript:', 'mailto:', 'ftp:', 'tcp:', 'ws:', 'wss:', 'tencent:',
           'email:', '#']
web_encoding = None

# 锁
html_url_lock = threading.Lock()
already_download_html_lock = threading.Lock()

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
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0",
    "Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:27.0) Gecko/20121011 Firefox/27.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0",
    "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0",
    "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0",
    "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0",
    "Mozilla/5.0 (Microsoft Windows NT 6.2.9200.0); rv:22.0) Gecko/20130405 Firefox/22.0",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:21.0.0) Gecko/20121011 Firefox/21.0.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (X11; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20130514 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130330 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130331 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0",
    "Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/19.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/18.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6",
    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",

]


def remove_dirs(url: str) -> str:
    return url.replace('\\\\\\\\', '\\').replace('\\\\\\', '\\').replace('\\\\', '\\')


def create_path(file: str) -> str:
    '''
    创建文件夹
    '''
    path = os.getcwd() + f"\\{file}"
    path = remove_dirs(path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def random_headers():
    return {
        'user-agent': random.choice(list_useragent)
    }


def is_https(url: str) -> bool:
    '''
    是否是 http 获取 https 请求
    '''
    return re.match(r'^(http|https)://.*', url, re.I) is not None


def get_root_url(url: str) -> str:
    '''
    获取 根域名
    '''
    ls = url.split('/')
    return ls[0] + "//" + ls[2]


def get_domain_url(url: str) -> str:
    '''
    获取 domain
    '''
    return get_root_url(url).replace('https://', '').replace('http://', '')


def get_absolute_path(url: str) -> str:
    '''
    获取绝对路径
    '''
    url = url.replace('../', '').replace('./', '')
    if len(url) != 0 and url[0] != '/':
        url = f'/{url}'
    return f'{root_url}{url}'


def get_file_name(url: str) -> str:
    '''
    获取文件名
    '''
    url = url.replace('https://', '').replace("http://", '').replace(f'{domain}', '')
    filename = ''
    if "?" in url:
        res = re.match(f'.*/(.*)\.(.*)\?.*', url, re.I)
        try:
            filename = f'{res.group(1)}.{res.group(2)}'
        except:
            if "/" in filename:
                filename = filename.split("/")[-1]
            else:
                filename = ''
        if "?" in filename:
            filename = filename.split("?")[0]
    else:
        res = re.match(f'.*/(.*)\.(.*).*', url, re.I)
        try:
            filename = f'{res.group(1)}.{res.group(2)}'
        except:
            if "/" in filename:
                filename = filename.split("/")[-1]
            else:
                filename = ''
    return filename


def get_file_ext(url: str) -> str:
    '''
    获取文件后缀
    '''
    filename = get_file_name(url)
    if "." in filename:
        return filename.split('.')[-1]
    return filename


def is_img_url(url: str) -> bool:
    '''
    是否是图片地址
    '''
    # 排除 base64 编码
    if url.startswith("data:"):
        return False
    return re.match(r'.*(\.(png|jpg|jpeg|apng|avif|bmp|gif|ico|cur|svg|tiff|webp)).*', url, re.I) is not None


def is_html_url(url: str) -> bool:
    '''
    是否是html地址
    '''
    if url.startswith("//"):
        return False
    if url == '/' or url == '' or root_url == url or url == f'{root_url}/':
        return True
    # 一般认为 html 请求不带后缀
    if get_file_ext(url) == '':
        return True
    return re.match(r'.*(\.(html|htm|xhtml|shtml|php|asp|jsp|jspx|md|erb|twig)).*$', url,
                    re.I) is not None


def is_css_url(url: str) -> bool:
    '''
    是否是css地址
    '''
    if url.startswith("//"):
        return False
    return re.match(r'.*(\.(css)).*$', url, re.I) is not None


def is_js_url(url: str) -> bool:
    '''
    js
    '''
    if url.startswith("//"):
        return False
    return re.match(r'.*(\.(js)).*$', url, re.I) is not None


def is_font_url(url: str) -> bool:
    '''
    字体
    '''
    if url.startswith("//"):
        return False
    return re.match(r'.*(\.(ttf|otf|woff|woff2)).*$', url, re.I) is not None


def is_video_url(url: str) -> bool:
    '''
    video
    '''
    if url.startswith("//"):
        return False
    return re.match(r'.*(\.(mp4|mov|avi|wmv|flv|mkv|webm|3gp|3g2|rm|rmvb|mepeg|mpg|vob|ts|mts|divx'
                    r'|ogb|h264|h265)).*$', url, re.I) is not None


def is_audio_url(url: str) -> bool:
    '''
    audio
    '''
    if url.startswith("//"):
        return False
    return re.match(r'.*(\.(mp3|wav|flac|aac|ogg|m4a|wma|ape|mid|midi|amr)).*$', url, re.I) is not None


def is_same_url(url: str) -> bool:
    '''
    TODO 是否是相似地址
    '''
    if is_html_url(url):
        # with already_download_html_lock:
        return url in already_download_html_list
    elif is_css_url(url):
        return url in already_download_css_list
    elif is_js_url(url):
        return url in already_download_js_list
    elif is_font_url(url):
        return url in already_download_font_list
    elif is_img_url(url):
        return url in already_download_img_list
    elif is_audio_url(url):
        return url in already_download_audio_list
    elif is_video_url(url):
        return url in already_download_video_list

    #  TODO 是否是相似地址 此处应该有更严密判断逻辑 对于相似的地址不应该多次下载
    #  TODO 比如 /page/1/index.html /page/2/index.html /page/3/index.html
    #  TODO 比如 /index_1.html /index_2.html /index_3.html
    #  对于以上相似的 不应重复下载 只需下载一次或者两次就够了！！！
    #  ... 待完善
    return False


def is_local_domain_url(url: str) -> bool:
    '''
    是否是当前域名地址
    '''
    if url.startswith("://") or url.startswith("//"):
        return False
    if url.startswith("#"):
        return False
    # 如果没有 domain 同时也不是 https 或 http 链接说明是本站地址
    # 就算是本站地址 如果是 https 开头的资源就没有必要下载了！
    if is_https(url):
        return False
    if url == '/' or url == '' or url == root_url or url == f'{root_url}/':
        return True
    if domain in url:
        return True
    flag = True
    # 判断需要排除的链接是否在其中
    for p in exclude:
        if url.startswith(p):
            return False
    return flag


def append_list(url: str, l1: list) -> bool:
    if url in l1:
        return True
    l1.append(url)
    return False


def init_html_ext(url: str):
    if "True" not in is_get_file_ext:
        ext = get_file_ext(url)
        if ext != '':
            is_get_file_ext.append("True")
            file_ext[0] = f'.{ext}'


def is_already_download(url: str) -> bool:
    '''
    判断是否是对应地址 以及 是否需要存放
    '''
    if url is None or is_local_domain_url(url) is False:
        return True
    if domain not in url:
        url = get_absolute_path(url)
    url = check_download_url(url)
    if is_same_url(url):
        return True
    if is_html_url(url):
        # 分析文件后缀
        init_html_ext(url)
        # with html_url_lock:
        return append_list(url, html_url_list)
    elif is_css_url(url):
        return append_list(url, css_url_list)
    elif is_js_url(url):
        return append_list(url, js_url_list)
    elif is_img_url(url):
        return append_list(url, img_url_list)
    elif is_font_url(url):
        return append_list(url, font_url_list)
    elif is_audio_url(url):
        return append_list(url, audio_url_list)
    elif is_video_url(url):
        return append_list(url, video_url_list)
    else:
        return True


def replace_remove_url_dirs(url: str) -> str:
    url = url.replace('////', '/').replace('///', '/')
    if "#" in url:
        return url.split("#")[0]
    return url


def check_download_url(url: str):
    ext = get_file_ext(url)
    if ext == '':
        url = f'{url}/index{file_ext[0]}'
    if is_https(url):
        return replace_remove_url_dirs(url)
    elif domain in url:
        url = url.split(domain)[-1]
    if url[0] != '\\':
        url = f'\\{url}'
    return replace_remove_url_dirs(f'{root_url}{url}')


def parse_css_url(css_str):
    try:
        css_str = str(css_str)
        urls = re.findall(r"url\(['\"](.*?)['\"]\)", css_str, re.I | re.S)
        if urls:
            return urls
        else:
            return []
    except:
        return []


def response_html(url: str, is_wb_file=False, is_css_or_js=False):
    '''
    对链接 响应
    '''
    global web_encoding
    text_content = None
    html = None
    try:
        time.sleep(random.random() * max_sleep_time)  # 添加休眠时间，防止访问服务器被封
        data = requests.get(url=url, headers=random_headers(), verify=True, timeout=10)
        if data.status_code == 200:
            if is_wb_file:
                return data
            if is_css_or_js:
                return {
                    'text': data.content.decode('UTF-8'),
                    'html': None
                }
            # 是否首次匹配 如果是首次匹配到了网页编码
            try:
                if web_encoding is None:
                    web_encoding = re.search(r'.* charset="(.*?)".*', data.text, re.I)[1]
            except:
                pass
            if web_encoding is None:
                try:
                    text_content = data.content.decode('UTF-8')
                    web_encoding = "UTF-8"
                except:
                    text_content = data.content.decode('GBK')
                    web_encoding = "GBk"
            else:
                try:
                    text_content = data.content.decode(web_encoding)
                except:
                    if web_encoding == 'gbk':
                        text_content = data.content.decode('UTF-8')
                        web_encoding = "UTF-8"
                    else:
                        text_content = data.content.decode('gbk')
                        web_encoding = "gbk"
                        # 如果没有获取到编码
            if is_html_url(url) or len(already_download_html_list) == 0:
                try:
                    html = BeautifulSoup(text_content, 'html.parser')
                except:
                    pass
        return {
            'html': html,
            'text': text_content
        }
    except Exception as e:
        print(f"响应失败！{url} error = {e}")
        return None


def parse_save_local_all_urls(links: list, soup: BeautifulSoup, tag_name: str, link_attr: str):
    try:
        for a_tag in soup.find_all(tag_name, attrs={link_attr: True}):
            links.append(a_tag[link_attr])
    except:
        pass


def parse_media(html: BeautifulSoup, media_tag="video", source="source", src="src"):
    '''
    解析 media 类型标签
    '''
    links = html.select(media_tag)
    for tag in links:
        try:
            if tag:
                source_tag = tag.find(source)
                if source_tag and src in source_tag.attrs:
                    is_already_download(source_tag[src])
        except Exception as e:
            print(f"解析 {media_tag} 异常 {e}")


def parse_urls(soup: BeautifulSoup | str):
    if hasattr(soup, "find_all") and callable(getattr(soup, "find_all")):
        links = []
        thread1 = threading.Thread(target=parse_save_local_all_urls, args=(links, soup, "a", "href"))
        thread2 = threading.Thread(target=parse_save_local_all_urls, args=(links, soup, "script", "src"))
        thread3 = threading.Thread(target=parse_save_local_all_urls, args=(links, soup, "link", "href"))
        thread4 = threading.Thread(target=parse_save_local_all_urls, args=(links, soup, "img", "src"))
        thread5 = threading.Thread(target=parse_save_local_all_urls, args=(links, soup, "video", "src"))
        thread6 = threading.Thread(target=parse_save_local_all_urls, args=(links, soup, "audio", "src"))

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()

        css_str = str(soup.find_all('style'))
        new_list = parse_css_url(css_str)
        for css_text in new_list:
            if css_text is not None and css_text != '':
                links.append(css_text)

        # 等待
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()
        # 处理所有链接

        for link in links:
            is_already_download(link)


def clone_list(url_list: list):
    '''
    拷贝 list
    :param url_list:
    :return:
    '''
    new_list = []
    if type(url_list) == list and len(url_list) != 0:
        for i in url_list:
            new_list.append(i)
    return new_list


def get_replace_path_f(path: str):
    return path.replace('https://', '').replace('http://', '').replace('/', '\\').replace('\\\\\\',
                                                                                          '\\')


def get_full_path(url):
    '''
    获取文件完整路径
    :param url:
    :return:
    '''
    try:
        fileName = get_file_name(url)
        if "?" in fileName:
            fileName = re.match(r'(.*)\?.*', fileName, re.I)[1]
        path = get_replace_path_f(url.split(fileName)[0])
        fullPath = f'{create_path(path)}\\{fileName}'
        return remove_dirs(fullPath)
    except:
        path = get_replace_path_f(url)
        fullPath = f'{create_path(path)}\\index{file_ext[0]}'
        return remove_dirs(fullPath)


def start_download_text_file(url, is_css_or_js=False):
    '''
    下载 html css js 文件
    '''
    res = response_html(url, False, is_css_or_js)
    try:
        if res is None or res['text'] is None:
            if len(already_download_html_list) == 0:
                print("请输入正确地址 或者尝试其他地址~")
            return
    except:
        return
    if not is_css_or_js or is_html_url(url) or len(already_download_html_list) == 0:
        if 'html' in res:
            parse_urls(res['html'])
    # 解析css或者js中 url
    if is_css_or_js:
        new_urls = parse_css_url(res['text'])
        for new_url in new_urls:
            is_already_download(new_url)
    try:
        fullpath = get_full_path(url)
        print(f'{fullpath}')
        with open(fullpath, mode='w', encoding="utf-8") as file:
            file.write(res['text'])
    except Exception as e:
        print(f"文本文件 {url} 写入失败 {e}")
    return res


def start_download_wb_file(url):
    '''
    下载二进制文件
    '''
    res = response_html(url, True)

    if res is None:
        return

    try:
        fullpath = get_full_path(url)
        print(f'{fullpath}')
        with open(fullpath, mode='wb') as file:
            try:
                file.write(res.content)
            except:
                pass
    except Exception as e:
        print(f"二进制文件 {url} 写入失败 {e}")


def download_list(msg: str, url_list: list, already_download_list: list, is_css_or_js: bool):
    if len(url_list) != 0:
        # print(f"==================开始下载{msg}文件==================")
        new_list = clone_list(url_list)
        for url in new_list:
            num = 0
            if len(new_list) <= 10:
                num = len(new_list)
            else:
                num = 10
            if url not in already_download_list:
                with ThreadPoolExecutor(max_workers=num) as executor:
                    if is_css_or_js:
                        executor.submit(start_download_text_file, url, True)
                    else:
                        executor.submit(start_download_wb_file, url)
                    url_list.remove(url)
                    already_download_list.append(url)


def download_other():
    '''
    下载其他文件
    '''
    try:
        thread1 = threading.Thread(target=download_list, args=('css', css_url_list, already_download_css_list, True))
        thread2 = threading.Thread(target=download_list, args=('js', js_url_list, already_download_js_list, True))
        thread3 = threading.Thread(target=download_list, args=('img', img_url_list, already_download_img_list, False))
        thread4 = threading.Thread(target=download_list,
                                   args=('font', font_url_list, already_download_font_list, False))
        thread5 = threading.Thread(target=download_list,
                                   args=('audio', audio_url_list, already_download_audio_list, False))
        thread6 = threading.Thread(target=download_list,
                                   args=('video', video_url_list, already_download_video_list, False))

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()

        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()
    except Exception as e:
        print("多线程下载异常 {e}")


def is_download_only_one_page() -> bool:
    return only_download_this_page == '1' \
        or only_download_this_page == 'y' \
        or only_download_this_page == 'Y' \
        or only_download_this_page == ''


def parse_page(url):
    '''
    解析
    '''
    if url not in already_download_html_list:
        try:
            start_download_text_file(url)
            # with already_download_html_lock:
            already_download_html_list.append(url)
            # with html_url_lock:
            if url in html_url_list:
                html_url_list.remove(url)
            if is_download_only_one_page():
                download_other()
            else:
                if mode == '1':
                    download_other()
                if mode == '2' and len(html_url_list) == 0 and len(already_download_html_list) != 0:
                    download_other()
                    print("=================下载完毕==============================")
                    return
                if len(html_url_list) == 1 and (html_url_list[0] == url or html_url_list[0] == root_url):
                    print("=================下载完毕==============================")
                    return
                if not is_download_only_one_page():
                    if is_html_url(url) or len(already_download_html_list) == 0:
                        # with html_url_lock:
                        for next_url in html_url_list:
                            parse_page(next_url)
                            # 使用线程池执行任务
                            # with ThreadPoolExecutor(max_workers=10) as executor:
                            #     executor.submit(parse_page, next_url)
        except Exception as e:
            print("解析异常:{}".format(e))


def clear_all():
    '''
    清空
    '''
    html_url_list.clear()
    css_url_list.clear()
    js_url_list.clear()
    img_url_list.clear()
    font_url_list.clear()
    audio_url_list.clear()
    video_url_list.clear()
    already_download_html_list.clear()
    already_download_css_list.clear()
    already_download_js_list.clear()
    already_download_img_list.clear()
    already_download_font_list.clear()
    already_download_video_list.clear()
    already_download_audio_list.clear()


def run():
    '''
    入口
    '''
    print("****************************使用须知************************")
    print("1、不支持单页面应用！！！")
    print("2、推荐下载整个网站源码 比较慢")
    print("3、兼容性问题 由于测试有限 所有不能一一兼顾到！")
    print("4、相似网页无法判断！比如 /page/1 /page/2 或者 /index_1.html /index_2.html ，会导致无法终结！")
    print("**********************************************************")
    global root_url
    global domain
    global mode
    global only_download_this_page
    global max_sleep_time
    while True:
        url = input('请输入域名地址: 如 http://dianshixinxi.com/ (默认) : ')
        # 设置 root 地址
        if url == '':
            url = 'http://dianshixinxi.com/'
        if re.match(r'^(https|http)://.*', url, re.I) is None:
            continue
        root_url = get_root_url(url)
        print("当前网站地址:", root_url)
        # 下载的文件夹就是以为 domain 根文件夹
        domain = get_domain_url(url)
        print("存放根目录文件名:", domain)
        only_download_this_page = input(
            '仅下载该链接（默认 推荐使用该方式！）; 输入任意其他字符为下载整个网站源码！')

        if not is_download_only_one_page():
            mode = input(
                '请选择下载模式 1、先下载单页面内容 (默认 页面较多)  2、先下载所有html再下载，其他其他资源 (在页面较少推荐使用该方式)  :')
            if mode != '2':
                mode = '1'
        if is_download_only_one_page():
            print(f"需要下载的页面地址为:{url} ")
        else:
            print(f"即将下载 {root_url} 网站源码 需要耐心等待！")
            if mode != '2':
                print("选择模式为下载所有html完毕之后在下载 其他资源")
            else:
                print('选择模式为下载选下载一个页面所有内容包括静态资源 !')
        try:
            max_sleep_time = int(
                input('单个链接最大休眠时间【防止被网站封禁 默认最大为 2s 】 输入 0-5 之间数字 超过5 将设置为5:'))
            if max_sleep_time < 0:
                max_sleep_time = 0
            elif max_sleep_time > 5:
                max_sleep_time = 5
        except:
            max_sleep_time = 2
        print(f"休眠最大时间为: {max_sleep_time}s")
        print("**************************任务开始****************************")
        parse_page(url)
        clear_all()
        print("*************************************************************")
        answer = input("本次任务已经完成！是否继续y? 输入y继续: ")
        if answer == 'y' or answer == "Y":
            continue
        else:
            print("\n拜拜!\n")
            break


if __name__ == '__main__':
    run()
