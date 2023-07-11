# 输入连接获取网站全部内容

### 构思

- 匹配页面链接
- 请求文件

### 使用方式

```shell
https://www.badiu.com
```


### 思路分析

输入的地址 获取页面全部链接内容
 - html
 - css
 - js
 - img
 - video
 - audio

将上面内容获取完毕后存储到数组中

此时数组应该是
- html_list
- css_list
- js_list
- ...


关键性问题

如果是获取 html 页面 需要分析是否是下一页，防止页面过多 ……