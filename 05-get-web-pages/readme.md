# 输入连接获取网站全部内容

### 灵感来源

于一些比较喜爱的网站 没有源码就很难受

### 核心思路

匹配页面全部链接,对全部链接做出响应

比如 获取页面全部链接内容
 - html
 - css
 - js
 - ...

将上面内容获取完毕后存储到数组中,请求过程中需要判断是否已经下载了

此时数组应该是
- html_list
- css_list
- js_list
- ...

### 打包

```shell
 pyinstaller --onefile index.py --name=get_web_page --icon=icon.png
```

### 使用方式

```shell
https://www.badiu.com
```



核心函数
```python
def parse_page(url):
    if url not in already_download_html_list:
        if len(already_download_html_list) == 0:
            print("=================开始下载 html 文件 =====================")
        try:
            start_download_text_file(url)
            with  already_download_html_lock:
                already_download_html_list.append(url)
            with html_url_lock:
                if url in html_url_list:
                    html_url_list.remove(url)
            if mode == '2':
                download_other()
            if mode == '1' and len(html_url_list) == 0 and len(already_download_html_list) != 0:
                download_other()
                print("=================下载完毕==============================")
                return
        except Exception as e:
            pass
        if is_html_url(url) or len(already_download_html_list) == 0:
            for next_url in html_url_list:
                # 使用线程池执行任务
                with ThreadPoolExecutor(max_workers=10) as executor:
                    executor.submit(parse_page, next_url)
```

然后通过遍历链接方式递归请求

### 终止条件

html_list 长度为0 说明解析过程中没用解析到链接了


### 存在问题

> 问题一 无法终止或者下载时间久

这个问题核心函数是`is_same_url()` 的实现 详情分析见 TODO 部分，


```python
def is_same_url(url: str) -> bool:
    '''
    TODO 是否是相似地址
    '''
    if is_html_url(url):
        with already_download_html_lock:
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
    return False
```

如果一个页面下一页内容过多会导致下载很久，但是这些页面大致相似，根本不需要重复下载

难点在于如何判断这个链接是否是下一页链接或者与其他页面相似,不同页面对于重复链接

> 问题二 

对于测试网站有限兼容性存在问题,对于一些网站可能是无法下载

> 问题三

单页面应用目前不支持!!!