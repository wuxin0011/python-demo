import os.path
import re

# url = 'https://www.baidu.com/about/index.html'
# url1 = 'https://www.baidu.com/index.js'
# url2 = 'http://www.baidu.com/index.js'
# url3 = 'http://www.baidu.com/index.js'
#
# result = re.search(r'(.*)/.*?', 'http://www.czgrl.cn/article/news.html', re.I)
#
# print("域名:", 'http://www.czgrl.cn/anews.html'.split('/')[0] + 'http://www.czgrl.cn/anews.html'.split('/')[2])
# # print("域名:", re.search(r'(.*)/.*', result, re.I).group(1))
#
# print(re.search(r'.*\.html', url, re.I))
# print(re.search(r'.*\.html', url1, re.I))
# print(re.search(r'.*\.js', url, re.I))
# print(re.search(r'.*\.js', url1, re.I))
#
# print(re.match(r'^(http|https)://.*', url2, re.I))
#
# # 匹配文件名
# url = 'https://www.baidu.com/index.html?keywords=100'
# file_name = re.findall(r'^(http|https)://.*/(.*)\.(.*).*$', url, re.I)
#
# file = re.match(r'^(http|https)://.*(\.(js)).*$', url1, re.I)
# if file:
#     print("匹配到js文件")
# else:
#     print("匹配js失败！")
#
# if file_name:
#     print('获取文件名', file_name[0][1])
#     print('文件后缀', file_name[0][2])
#     ext = file_name[0][2]
#     if ext:
#         ext = re.search(r'(.*)\?.*', ext, re.I)
#         print("ext", ext.group(1))
# else:
#     print('无法从链接中获取文件名')
#
# # url1 = 'https://www.baidu.com/index.html?keyworld="hello world"&&username="username"'
# url1 = 'https://www.toolnb.com/Public/common/js/common.js?v2023070820'
# url1 = 'https://www.toolnb.com/Public/common/js/common.js'
# # url1 = url1.replace('https://','').replace('http://','')
# file_name = os.path.basename(url1)
#
# if file_name:
#     if '?' in file_name:
#         print("filename? = ", re.match(r'(.*)\?.*', file_name, re.I)[1])
#     else:
#         print("filename = ", file_name)
#
# else:
#     print('无法从链接中获取文件名')
#
# print("匹配图片地址")
#
# str1 = 'png|jpg|jpeg|apng|avif|bmp|gif|ico|cur|svg|tiff|webp'.split('|')
# print(str1)
#
# isAllSuccess = True
# for i in str1:
#     res = re.match(r'.*(\.(png|jpg|jpeg|apng|avif|bmp|gif|ico|cur|svg|tiff|webp)).*',
#                    f'https://www.badiu.com/index.{i}', re.I)
#     if res is None:
#         print("")
#         isAllSuccess = False
#         break;
# if isAllSuccess:
#     print("全部匹配")
# else:
#     print("匹配失败！")
#
# urls = ['https://www.baidu.com']
#
# print(re.match(r'^(http|https)://(.*)', '/static/4/news.css', re.I))

# print('https://www.baidu.com' in urls)
# print(url in urls)

l1 = []
print('l1' in l1)


# if 'l2' in l1 :
#     l1.remove('l2')
#     print(l1)


# def get_file_extension(file_path):
#     _, file_extension = os.path.splitext(file_path)
#     return file_extension
#
#
# print('e',get_file_extension('https://mycolor.space/index') == '')


def get_absolute_path(url1: str, url2: str):
    url2 = url2.replace('../', '').replace('./', '')
    if url2[0] != '/':
        url2 = f'/{url2}'
    return f'{url1}{url2}'


def get_file_name(url: str):
    url = url.replace('https://', '').replace("http://", '').replace('www.baidu.com', '')
    filename = ''
    # if "?" in url:
    #     res = re.match(f'.*/(.*)\.(.*)\?.*', url, re.I)
    #     try:
    #         filename = f'{res.group(1)}.{res.group(2)}'
    #     except:
    #         if "/" in filename:
    #             pass
    #         else:
    #             pass
    #     if "?" in filename:
    #         filename = filename.split("?")[0]
    # else:
    res = re.match(f'.*/(.*)\.(.*).*', url, re.I)
    try:
        filename = f'{res.group(1)}.{res.group(2)}'
    except:
        if "/" in filename:
            filename = filename.split('/')[-1]
        else:
            filename = ''
    return filename


def get_file_ext():
    pass


print(get_file_name("https://www.baidu.com/about/index/index.htmdex.html"))
print(get_file_name("https://www.baidu.com/about/index/index.html?keyworkd=index.html?docker=?docker"))
print(get_file_name("https://www.baidu.com"))
print(get_file_name("https://www.baidu.com/"))
print(get_file_name("https://www.baidu.com/?"))

s1 = 'D:\\desktop\\github\python-demo\\05-get-web-pages\\www.czgrl.cn\\'.replace(r"\\", '')

if s1[-1] == '\\':
    s1 = s1[:-1]
print(s1)
