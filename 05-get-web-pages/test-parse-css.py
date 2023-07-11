'''
解析 css 中 backgorund url
'''
import re

css_str = '''


@media screen and (max-width:414px) and (min-width:400px) {

    .svg-position{

        left: 37% !important;
        background:url('https://baidu.com/index.png');

    }

}

@media screen and (max-width:768px) and (min-width:758px) {

    .svg-position{

        left: 20% !important;
         background:url('https://baidu.com/index1.png');

    }

}

@media screen and (max-width:259px) {

    .svg-position{

        left: 28% !important;
         background:url('https://baidu.com/index2.png');
         background:url('/index3.png');
    }

}


'''

urls = re.findall(r"url\(['\"](.*?)['\"]\)", css_str, re.I | re.S)
if urls:
    for url in urls:
        print(url)
else:
    print("未找到匹配的内容")