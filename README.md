# python-demo

#### 介绍
python简单使用
#### 安装镜像源头，加速下载
 - 清华云:https://pypi.tuna.tsinghua.edu.cn/simple
 - 阿里云:http://mirrors.aliyun.com/pypi/simple/
 - 中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/
 - 华中理工大学:http://pypi.hustunique.com/
 - 山东理工大学:http://pypi.sdutlinux.org/ 
 - 豆瓣:http://pypi.douban.com/simple/
> 使用方式如下

~~~shell
pip install 包名 -i 镜像源地址

#例如安装 pandas
pip install pandas -i http://pypi.douban.com/simple/
~~~


>永久修改制定地址

**Linux**
 - 查看是否存在文件 /etc/pip.conf
    ~~~shell
    touch /etc/pip.conf
    
    ~~~
 - 进入配置文件修改：`vim /etc/pip.conf`
    ~~~shell
    [global]
    index-url = https://pypi.douban.com/simple
    # 如果使用http链接，则需要trusted-host参数
    [install]
    trusted-host = mirrors.aliyun.com
    ~~~


**windows**
 - win+r 打开命令面板
 - %HOMEPATH% 进入配置 创建文件夹 pip 然后创建 pip.ini
 - ~~~shell
    [global]
    timeout = 6000
    index-url = https://pypi.douban.com/simple
    trusted-host = mirrors.aliyun.com
   ~~~