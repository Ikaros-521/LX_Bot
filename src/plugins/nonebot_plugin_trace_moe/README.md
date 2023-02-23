<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_trace_moe
  
_✨ NoneBot 基于trace.moe的动画截图场景追溯插件 ✨_
  
<a href="https://github.com/Ikaros-521/nonebot_plugin_trace_moe/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Ikaros-521/nonebot_plugin_trace_moe?color=%09%2300BFFF&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_trace_moe/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Ikaros-521/nonebot_plugin_trace_moe?color=Emerald%20green&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_trace_moe/network">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/Ikaros-521/nonebot_plugin_trace_moe?color=%2300BFFF&style=flat-square">
</a>
<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Ikaros-521/nonebot_plugin_trace_moe.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_trace_moe">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_trace_moe.svg" alt="pypi">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</a>

</div>

适用于nonebot2 v11的基于trace.moe的动画截图场景追溯插件  
调用的相关API源自:https://soruly.github.io/trace.moe-api/#/  
ps:查询结果可能会有H，请自行注意  

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## 目录

- [nonebot_plugin_trace_moe](#nonebot_plugin_trace_moe)
  - [🔧 开发环境](#-%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83)
  - [💿 安装](#-%E5%AE%89%E8%A3%85)
    - [1. nb-cli安装（推荐）](#1-nb-cli%E5%AE%89%E8%A3%85%E6%8E%A8%E8%8D%90)
    - [2. 本地安装](#2-%E6%9C%AC%E5%9C%B0%E5%AE%89%E8%A3%85)
    - [3. pip安装](#3-pip%E5%AE%89%E8%A3%85)
    - [更新版本](#%E6%9B%B4%E6%96%B0%E7%89%88%E6%9C%AC)
  - [🔧 配置](#-%E9%85%8D%E7%BD%AE)
    - [env配置](#env%E9%85%8D%E7%BD%AE)
  - [🎉 功能](#-%E5%8A%9F%E8%83%BD)
  - [👉 命令](#-%E5%91%BD%E4%BB%A4)
    - [1、先发送命令，再发送图片（命令前缀请自行替换）](#1%E5%85%88%E5%8F%91%E9%80%81%E5%91%BD%E4%BB%A4%E5%86%8D%E5%8F%91%E9%80%81%E5%9B%BE%E7%89%87%E5%91%BD%E4%BB%A4%E5%89%8D%E7%BC%80%E8%AF%B7%E8%87%AA%E8%A1%8C%E6%9B%BF%E6%8D%A2)
    - [2、命令+图片](#2%E5%91%BD%E4%BB%A4%E5%9B%BE%E7%89%87)
    - [3、回复图片+命令](#3%E5%9B%9E%E5%A4%8D%E5%9B%BE%E7%89%87%E5%91%BD%E4%BB%A4)
  - [⚙ 拓展](#-%E6%8B%93%E5%B1%95)
  - [📝 更新日志](#-%E6%9B%B4%E6%96%B0%E6%97%A5%E5%BF%97)
  - [致谢](#%E8%87%B4%E8%B0%A2)
  - [项目打包上传至pypi](#%E9%A1%B9%E7%9B%AE%E6%89%93%E5%8C%85%E4%B8%8A%E4%BC%A0%E8%87%B3pypi)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## 🔧 开发环境
Nonebot2：2.0.0b5  
python：3.8.13  
操作系统：Windows10（Linux兼容性问题不大）  
编辑器：pycharm  

## 💿 安装
环境依赖`aiohttp、asyncio`库   

### 1. nb-cli安装（推荐）
在你bot工程的文件夹下，运行cmd（运行路径要对啊），执行nb命令安装插件，插件配置会自动添加至配置文件  
```
nb plugin install nonebot_plugin_trace_moe
```

### 2. 本地安装
先安装下 `aiohttp`  
```
pip install aiohttp
```
将项目clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的`src/plugins`），然后把`nonebot_plugin_trace_moe`文件夹里的内容拷贝至上一级目录即可。  
clone命令参考（得先装`git`，懂的都懂）：
```
git clone https://github.com/Ikaros-521/nonebot_plugin_trace_moe.git
``` 
也可以直接下载压缩包到插件目录解压，然后同样提取`nonebot_plugin_trace_moe`至上一级目录。  
目录结构： ```你的bot/src/plugins/nonebot_plugin_trace_moe/__init__.py```  


### 3. pip安装
```
pip install nonebot_plugin_trace_moe
```  
打开 nonebot2 项目的 ```bot.py``` 文件, 在其中写入  
```nonebot.load_plugin('nonebot_plugin_trace_moe')```  
当然，如果是默认nb-cli创建的nonebot2的话，在bot路径```pyproject.toml```的```[tool.nonebot]```的```plugins```中添加```nonebot_plugin_trace_moe```即可  
pyproject.toml配置例如：  
``` 
[tool.nonebot]
plugin_dirs = ["src/plugins"]
plugins = ["nonebot_plugin_trace_moe"]
``` 

### 更新版本
```
nb plugin update nonebot_plugin_trace_moe
```

## 🔧 配置  

### env配置
```
# nonebot_plugin_trace_moe
# 最大返回查询结果数
trace_moe_max_ret=3
# 自动撤回时间（秒）
trace_moe_withdraw_time=100
```
|       配置项        | 必填 | 默认值  |                      说明                      |
|:----------------:|:----:|:----:|:----------------------------:|
| `trace_moe_max_ret` | 否 | `3` | 最大返回查询结果数 |
| `trace_moe_withdraw_time` | 否 | `0` | 自动撤回延时（秒），为0是不撤回 |


## 🎉 功能
调用trace.moe的API查询动画截图源自的作品名和时间段  

## 👉 命令

### 1、先发送命令，再发送图片（命令前缀请自行替换）
先发送`/图片来源`或`/trace`或`/图片定位`，等bot返回`请发送需要识别的图片喵~`后，发送需要识别的图片即可。  

### 2、命令+图片
编辑消息`/图片来源[待识别的图片]`或`/trace[待识别的图片]`或`/图片定位[待识别的图片]`发送即可。  
bot返回内容：  
![](docs/result.png)  

### 3、回复图片+命令
回复需要处理的图片，发送`/图片来源`或`/trace`或`/图片定位`即可。  

## ⚙ 拓展
修改`__init__.py`中的`catch_str = on_command("图片来源", aliases={"trace", "图片定位"})`来自定义命令触发关键词。  

## 📝 更新日志

<details>
<summary>展开/收起</summary>

### 0.0.1

- 插件初次发布

### 0.0.2

- 向上兼容rc2  

### 0.0.3

- 可以通过回复图片触发  

### 0.0.4

- 插件补充元信息  
- 优化异常报错

### 0.1.0

- 实现自动撤回功能（保号）  

</details>

## 致谢

- [trace.moe](https://trace.moe) - API来源  

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
# poetry config pypi-token.pypi

# 1、安装poetry
pip install poetry

# 2、初始化配置文件（根据提示填写）
poetry init

# 3、微调配置文件pyproject.toml

# 4、运行 poetry install, 可生成 “poetry.lock” 文件（可跳过）
poetry install

# 5、编译，生成dist
poetry build

# 6、发布(poetry config pypi-token.pypi 配置token)
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