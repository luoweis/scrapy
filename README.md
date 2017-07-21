# 爬虫
## 安装
```
virtualenv --no-site-packages venv
source venv/bin/active
pip install Scrapy
```
### 创建一个scrapy项目
```
scrapy startproject scrapyTest
```

### 项目目录
```
scrapyTest/
├── scrapy.cfg  #配置文件
└── scrapyTest  #项目主目录
    ├── __init__.py
    ├── items.py    #定义项目文件
    ├── middlewares.py #中间件
    ├── pipelines.py    #管道
    ├── settings.py     #配置文件
    └── spiders         #爬虫文件
        └── __init__.py
```