'''
获取网站全部内容
'''
import os
import random
import re
import time

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
exclude = ['tel:', 'file:', 'data:', 'void(0)', 'javascript:', 'mailto:', 'ftp', 'tcp', 'ws:', 'wss']

is_flag = False


def create_path(file):
    '''
    创建文件夹
    :param file:
    :return:
    '''
    path = os.getcwd() + f"\\{domain}\\{file}"
    # path = path.replace(r'\\', '')
    # if path[-1] == '\\':
    #     path = path[:-1]
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def random_headers():
    '''
    随机请求头
    :return:
    '''
    return {
        'user-agent': random.choice(list_useragent)
    }


def is_https(url):
    '''
    是否是 http 获取 https 请求
    :param url:
    :return:
    '''
    return re.match(r'^(http|https)://.*', url, re.I) is not None


def get_root_url(url):
    '''
    获取 根域名
    :param url:
    :return:
    '''
    ls = url.split('/')
    return ls[0] + "//" + ls[2]


def get_domain_url(url):
    '''
    获取 domain
    :param url:
    :return:
    '''
    return get_root_url(url).replace('https://', '').replace('http://', '')


def get_absolute_path(url: str):
    '''
    获取绝对路径
    :param url:
    :return:
    '''
    url = url.replace('../', '').replace('./', '')
    if url[0] != '/':
        url = f'/{url}'
    return f'{root_url}{url}'


def get_file_name(url):
    '''
    获取文件名
    :param url:
    :return:
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


def get_file_ext(url):
    '''
    获取问价后缀
    :param url:
    :return:
    '''
    filename = get_file_name(url)
    if "." in filename:
        return filename.split('.')[-1]
    return filename


def is_img_url(url):
    '''
    是否是图片地址
    :param url:
    :return:
    '''
    return re.match(r'.*(\.(png|jpg|jpeg|apng|avif|bmp|gif|ico|cur|svg|tiff|webp)).*', url, re.I) is not None


def is_html_url(url):
    '''
    是否是html地址
    :param url:
    :return:
    '''
    if url == '/' or url == '' or url == f'{root_url}/' or url == f'{root_url}':
        return True
    return re.match(r'^(http|https)://.*(\.(html|htm|xhtml|shtml|php|asp|jsp|jspx|md|erb|twig)).*$', url,
                    re.I) is not None


def is_css_url(url):
    '''
    是否是css地址
    :param url:
    :return:
    '''
    return re.match(r'^(http|https)://.*(\.(css)).*$', url, re.I) is not None


def is_js_url(url):
    return re.match(r'^(http|https)://.*(\.(js)).*$', url, re.I) is not None


def is_font_url(url):
    return re.match(r'^(http|https)://.*(\.(ttf|otf|woff|woff2)).*$', url, re.I) is not None


def is_video_url(url):
    return re.match(r'^(http|https)://.*(\.(mp4|mov|avi|wmv|flv|mkv|webm|3gp|3g2|rm|rmvb|mepeg|mpg|vob|ts|mts|divx'
                    r'|ogb|h264|h265)).*$', url, re.I) is not None


def is_audio_url(url):
    return re.match(r'^(http|https)://.*(\.(mp3|wav|flac|aac|ogg|m4a|wma|ape|mid|midi|amr)).*$', url, re.I) is not None


def is_same_url(url):
    '''
    TODO 是否是相似地址
    :param url:
    :return:
    '''
    if url in already_download_html_list or \
            url in already_download_css_list or \
            url in already_download_js_list or \
            url in already_download_img_list or \
            url in already_download_font_list or \
            url in already_download_video_list or \
            url in already_download_audio_list:
        return True
    return False


def is_local_domain_url(url):
    '''
    是否是当前域名地址
    :param url:
    :return:
    '''
    if url == '/' or url == '' or url == root_url or url == f'{root_url}/':
        return True
    if domain in url:
        return True
    # 如果没有 domain 同时也不是 https 或 http 链接说明是本站地址
    if is_https(url):
        return False
    if url.startswith("#"):
        return False
    flag = True
    # 判断需要排除的链接是否在其中
    for p in exclude:
        if p in url:
            flag = False
            break
    return flag


def is_already_download(url):
    '''
    判断是否是对应地址 以及 是否需要存放
    :param url:
    :return:
    '''
    if url is None or is_local_domain_url(url) is False:
        return
    if domain not in url:
        url = get_absolute_path(url)
    if is_same_url(url):
        return
    if is_html_url(url) and url not in html_url_list:
        html_url_list.append(url)
        # 分析文件后缀
        if is_get_file_ext[0] == 'False':
            ext = get_file_ext(url)
            if ext != '':
                is_get_file_ext[0] == 'True'
                file_ext[0] = f'.{ext}'
        return False
    elif is_css_url(url) and url not in css_url_list:
        css_url_list.append(url)
        return False
    elif is_js_url(url) and url not in js_url_list:
        js_url_list.append(url)
        return False
    elif is_font_url(url) and url not in font_url_list:
        font_url_list.append(url)
        return False
    elif is_img_url(url) and url not in img_url_list:
        img_url_list.append(url)
        return False
    elif is_audio_url(url) and url not in audio_url_list:
        audio_url_list.append(url)
        return False
    elif is_video_url(url) and url not in video_url_list:
        video_url_list.append(url)
        return False
    else:
        return True


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


def response_html(url, isFile=False, is_css_or_js=False):
    '''
    对链接 响应
    :param url:
    :param isFile:
    :param is_css_or_js:
    :return:
    '''
    global web_encoding
    web_encoding = None
    text_content = None
    html = None
    try:
        time.sleep(random.random() * 3)  # 添加休眠时间，防止访问服务器被封
        data = requests.get(url=url, headers=random_headers(), verify=True)
        if data.status_code == 200:
            if isFile:
                return data.content
            if is_css_or_js:
                return {
                    'text': data.text,
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
        else:
            print("响应失败！")
        return {
            'html': html,
            'text': text_content
        }
    except Exception as e:
        print("响应失败！{}", e)
        return None


def parse_save_local_all_urls(links: list, soup: BeautifulSoup, tag_name: str, link_attr: str):
    for a_tag in soup.find_all(tag_name, attrs={link_attr: True}):
        links.append(a_tag[link_attr])


def parse_media(html: BeautifulSoup, media_tag="video", source="source", src="src"):
    '''
    解析 media 类型标签
    :param html:
    :param media_tag:
    :param source:
    :param src:
    :return:
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


def parse_urls(soup: BeautifulSoup):
    links = []
    parse_save_local_all_urls(links, soup, "a", "href")
    parse_save_local_all_urls(links, soup, "script", "src")
    parse_save_local_all_urls(links, soup, "link", "href")
    parse_save_local_all_urls(links, soup, "img", "src")
    parse_save_local_all_urls(links, soup, "video", "src")
    parse_save_local_all_urls(links, soup, "audio", "src")
    css_str = str(soup.find_all('style'))
    new_list = parse_css_url(css_str)
    for css_url in new_list:
        links.append(css_url)
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
    return path.replace('https://', '').replace('http://', '').replace(domain, '').replace('/', '\\').replace('\\\\\\',
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
        return fullPath
    except:
        path = get_replace_path_f(url)
        fullPath = f'{create_path(path)}\\index{file_ext[0]}'
        return fullPath


def start_download_text_file(url, is_css_or_js=False):
    '''
    下载 html css js 文件
    :param url:
    :param is_css_or_js:
    :return:
    '''
    res = response_html(url, False, is_css_or_js)
    if res is None:
        return
    if not is_css_or_js or is_html_url(url) or len(already_download_html_list) == 0:
        if 'html' in res and res["html"] is not None:
            parse_urls(res['html'])

    # 解析css或者js中 url
    if is_css_or_js:
        new_urls = parse_css_url(res['text'])
        for new_url in new_urls:
            is_already_download(new_url)
    try:
        if res['text'] is not None:
            fullpath = get_full_path(url)
            print(f'{fullpath}')
            with open(fullpath, mode='w', encoding="utf-8") as file:
                file.write(res['text'])
    except Exception as e:
        print(f"下载失败:{e}")
    return res


def start_download_wb_file(url):
    '''
    下载二进制文件
    :param url:
    :return:
    '''
    res = response_html(url, True)
    if res is None:
        if len(already_download_html_list) == 0:
            print("请输入正确地址 或者尝试其他地址~")
        return
    try:
        fullpath = get_full_path(url)
        print(f'{fullpath}')
        with open(fullpath, mode='wb') as file:
            file.write(res)
    except Exception as e:
        print(f"下载失败 {e}")


def download_list(msg: str, url_list: list, already_download_list: list, is_css_or_js: bool):
    if len(url_list) != 0:
        print(f"==================开始下载{msg}文件==================")
        new_list = clone_list(url_list)
        for url in new_list:
            if url not in already_download_list:
                if is_css_or_js:
                    start_download_text_file(url, True)
                else:
                    start_download_wb_file(url)
                url_list.remove(url)
                already_download_list.append(url)


def download_other():
    '''
    下载其他文件
    :return:
    '''
    download_list('css', css_url_list, already_download_css_list, True)
    download_list('js', js_url_list, already_download_js_list, True)
    download_list('img', img_url_list, already_download_img_list, False)
    download_list('font', font_url_list, already_download_font_list, False)
    download_list('audio', audio_url_list, already_download_audio_list, False)
    download_list('video', video_url_list, already_download_video_list, False)


def parse_page(url):
    '''
    解析
    :param url: 请求地址
    :return:
    '''
    if len(html_url_list) == 0 and len(already_download_html_list) != 0:
        if mode == '1':
            download_other()
        print("=================下载完毕==============================")
        return
    if url not in already_download_html_list:
        if mode == '1' and len(already_download_html_list) == 0:
            print("=================开始下载 html 文件 =====================")
        elif mode == '2':
            print("=================开始下载 html 文件 =====================")

        start_download_text_file(url)
        if mode == '2':
            download_other()
        try:
            already_download_html_list.append(url)
            if url in html_url_list:
                html_url_list.remove(url)
        except Exception as e:
            pass
        if is_html_url(url) or len(already_download_html_list) == 0:
            new_list = clone_list(html_url_list)
            for next_url in new_list:
                if next_url in html_url_list:
                    parse_page(next_url)


def clear_all():
    '''
    清空
    :return:
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


def run():
    '''
    入口
    :return:
    '''
    global root_url
    global domain
    global mode
    while True:
        url = input('请输入域名地址: 如 http://www.czgrl.cn/article/news.html : ')
        # 设置 root 地址
        if url == '':
            url = 'http://www.czgrl.cn/article/news.html'
        if re.match(r'^(https|http)://.*', url, re.I) is None:
            continue
        root_url = get_root_url(url)
        print("当前网站地址:", root_url)
        # 下载的文件夹就是以为 domain 根文件夹
        domain = get_domain_url(url)
        print("当前网站域名:", domain)
        mode = input('请选择下载模式 1、按照文件顺序下载 （默认） 2、按照下载顺序下载 :')
        if mode != '2':
            mode = '1'
            print('将采用默认顺序下载 !')
        parse_page(url)
        clear_all()
        answer = input("是否继续y? 输入y继续: ")
        if answer == 'y' or answer == "Y":
            continue
        else:
            print("\n拜拜!\n")
            break


if __name__ == '__main__':
    run()
