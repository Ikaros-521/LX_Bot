<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_searchInWeb
  
_✨ NoneBot 搜索引擎截图 ✨_
  
<a href="https://github.com/Ikaros-521/nonebot_plugin_searchInWeb/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Ikaros-521/nonebot_plugin_searchInWeb?color=%09%2300BFFF&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_searchInWeb/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Ikaros-521/nonebot_plugin_searchInWeb?color=Emerald%20green&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_searchInWeb/network">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/Ikaros-521/nonebot_plugin_searchInWeb?color=%2300BFFF&style=flat-square">
</a>
<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Ikaros-521/nonebot_plugin_searchInWeb.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_searchInWeb">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_searchInWeb.svg" alt="pypi">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</a>

</div>

适用于nonebot2 v11的搜索引擎截图

## 🔧 开发环境
Nonebot2：2.0.0b5  
python：3.8.13  
操作系统：Windows10（CentOS7下正常运行，Linux兼容性问题不大）  
编辑器：pycharm  

## 💿 安装
环境依赖`nonebot_plugin_htmlrender`库   


### 本地安装
先安装下 `htmlrender`  
```
pip install nonebot_plugin_htmlrender
```
将项目clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的`src/plugins`），然后把`nonebot_plugin_searchInWeb`文件夹里的内容拷贝至上一级目录即可。  
clone命令参考（得先装`git`，懂的都懂）：
```
git clone https://github.com/Ikaros-521/nonebot_plugin_searchInWeb.git
``` 
也可以直接下载压缩包到插件目录解压，然后同样提取`nonebot_plugin_searchInWeb`至上一级目录。  
目录结构： ```你的bot/src/plugins/nonebot_plugin_searchInWeb/__init__.py```  

## 🔧 配置

无

## 🎉 功能
传入搜索内容，使用对应搜索引擎进行搜索后，截图返回图片。  

## 👉 命令(命令前缀自行替换喵~)

### bd  （命令前缀自行添加）
命令结构：```/bd``` 或 ```/百度```  
例如：```/bd b站``` 或 ```/百度 python```  

### bing  （命令前缀自行添加）
命令结构：```/bing``` 或 ```/必应```  
例如：```/bing b站``` 或 ```/必应 python```  


## ⚙ 拓展


## 📝 更新日志

<details>
<summary>展开/收起</summary>

### 0.0.1

- 插件初次发布


</details> 

## 项目打包上传至pypi

官网：https://pypi.org，注册账号，在系统用户根目录下创建`.pypirc`，配置  
``` 
[distutils] 
index-servers=pypi 
 
[pypi] repository = https://upload.pypi.org/legacy/ 
username = 用户名 
password = 密码
```

### poetry

```
# 参考 https://www.freesion.com/article/58051228882/

# 1、安装poetry
pip install poetry

# 2、初始化配置文件（根据提示填写）
poetry init

# 3、微调配置文件pyproject.toml

# 4、运行 poetry install, 可生成 “poetry.lock” 文件（可跳过）
poetry install

# 5、编译，生成dist
poetry build

# 6、发布
poetry publish

```

### twine

```
# 参考 https://www.cnblogs.com/danhuai/p/14915042.html
#创建setup.py文件 填写相关信息

# 1、可以先升级打包工具
pip install --upgrade setuptools wheel twine

# 2、打包
python setup.py sdist bdist_wheel

# 3、可以先检查一下包
twine check dist/*

# 4、上传包到pypi（需输入用户名、密码）
twine upload dist/*
```
