## 简介
这个小程序抓取中国银行外汇牌价的数据， 网址：http://www.boc.cn/sourcedb/whpj/

然后统计一天中的每一个货币的最高现汇卖出价， 并生成个csv文件。

中国银行外汇牌价，这个网页只有前面10页的数据是有有效数据，所以这个小程序只抓取前面10页的数据。

## 环境设置

这个项目使用的是python34，不能使用python35，因为py2exe目前还不支持py35。

建议使用virtualenv建立单独的环境，下面是通过pip安装：
```
pip install virtualenv     # 安装virtualenv
```

进入项目的目录以后使用终端执行下面的命令，这里是以windows为例：
```
virtualenv .venv           # 创建这个项目的virtualenv环境
.venv\Script\active        # 激活virtualenv
pip install -r requirements.txt    # 安装这个项目依赖的包
```

## 打包使用py2exe

在命令行中运行下面的命令进行打包
```
.venv\Script\active
python setup.py py2exe
```