import re

import requests
from bs4 import BeautifulSoup

str1 = ''' 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.staticfile.org/twitter-bootstrap/5.1.1/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
	<link rel="stylesheet" href="/static/4/swiper-bundle.css">
	<link rel="stylesheet" href="/static/4/index.css">
    <link rel="stylesheet" href="/static/4/about.css">
    <title>å³äºæä»¬-å¸¸å·æ ¼çç«</title>
	<style type="text/css">
		
        @media  screen and (max-width:1400px){
    .input-block{
      display: none !important;
    }
}
@media  screen and (max-width:1399px){
	#feet-input-compent2{
        display: inline !important;
    }
}
@media  screen and (min-width:1400px) and (max-width:6000px){
    #feet-input-compent2{
        display: none !important;
    }
}
	</style>
</head>
<body>'''

print()

url = 'http://www.czgrl.cn/about.html'
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'}

def response_html(url,isFile = False):
    html = None
    try:
        data = requests.get(url=url, headers=headers)
        if data.status_code == 200:
            if isFile:
               return data.content
            encoding = re.search(r'.*<meta charset="(.*?)">.*', str1, re.I).group(1)
            print('encoding',encoding)
        else:
            print("响应失败！")
        return html
    except Exception as e:
        print("响应失败！{}", e)
        return None



# TEST
response_html('https://pic.netbian.com')
response_html('https://www.baidu.com/index.html')
response_html('http://www.czgrl.cn/article/news.html')
