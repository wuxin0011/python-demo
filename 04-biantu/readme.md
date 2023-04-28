### 打包测试

> 如果使用 `fake_useragent` 报错，升级
```shell
pip install -U fake_useragent
```

安装 python 打包依赖
```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller
```

执行打包
```shell
Pyinstaller -F -w -i xxx.ico yyyy.py

# 例如
Pyinstaller -F -w -i favicon.ico index.py
```

**注意路径问题**