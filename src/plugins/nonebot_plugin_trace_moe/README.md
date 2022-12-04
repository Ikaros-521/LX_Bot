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

## 🔧 开发环境
Nonebot2：2.0.0b5  
python：3.8.13  
操作系统：Windows10（Linux兼容性问题不大）  
编辑器：pycharm  

## 💿 安装
环境依赖`aiohttp`库   

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
TRACE_MOE_MAX_RET=3
```
|       配置项        | 必填 | 默认值  |                      说明                      |
|:----------------:|:----:|:----:|:----------------------------:|
| `TRACE_MOE_MAX_RET` | 否 | `""` | 最大返回查询结果数 |


## 🎉 功能
调用trace.moe的API查询动画截图源自的作品名和时间段  

## 👉 命令

### 1、先发送命令，再发送图片（命令前缀请自行替换）
先发送`/图片来源`或`/trace`或`/图片定位`，等bot返回`请发送需要识别的图片喵~`后，发送需要识别的图片即可。  

### 2、命令+图片
编辑消息`/图片来源[待识别的图片]`或`/trace[待识别的图片]`或`/图片定位[待识别的图片]`发送即可。 

## ⚙ 拓展
修改`__init__.py`中的`catch_str = on_command("图片来源", aliases={"trace", "图片定位"})`来自定义命令触发关键词。  

## 📝 更新日志

<details>
<summary>展开/收起</summary>

### 0.0.1

- 插件初次发布


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
# https://www.codenong.com/af301fe89b55706ca0c2/

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