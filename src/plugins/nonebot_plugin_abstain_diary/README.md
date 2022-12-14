<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_abstain_diary
  
_✨ NoneBot 戒色打卡日记 插件 ✨_
  
<a href="https://github.com/Ikaros-521/nonebot_plugin_abstain_diary/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Ikaros-521/nonebot_plugin_abstain_diary?color=%09%2300BFFF&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_abstain_diary/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Ikaros-521/nonebot_plugin_abstain_diary?color=Emerald%20green&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_abstain_diary/network">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/Ikaros-521/nonebot_plugin_abstain_diary?color=%2300BFFF&style=flat-square">
</a>
<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Ikaros-521/nonebot_plugin_abstain_diary.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_abstain_diary">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_abstain_diary.svg" alt="pypi">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</a>

</div>

适用于nonebot2 v11的戒色打卡日记插件    

## 🔧 开发环境
Nonebot2：2.0.0b5  
python：3.8.13  
操作系统：Windows10（Linux兼容性问题不大）  
编辑器：VS Code  

## 💿 安装

### 1. nb-cli安装（推荐）
在你bot工程的文件夹下，运行cmd（运行路径要对啊），执行nb命令安装插件，插件配置会自动添加至配置文件  
```
nb plugin install nonebot_plugin_abstain_diary
```

### 2. 本地安装
将项目clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的`src/plugins`），然后把`nonebot_plugin_abstain_diary`文件夹里的内容拷贝至上一级目录即可。  
clone命令参考（得先装`git`，懂的都懂）：
```
git clone https://github.com/Ikaros-521/nonebot_plugin_abstain_diary.git
``` 
也可以直接下载压缩包到插件目录解压，然后同样提取`nonebot_plugin_abstain_diary`至上一级目录。  
目录结构： ```你的bot/src/plugins/nonebot_plugin_abstain_diary/__init__.py```  


### 3. pip安装
```
pip install nonebot_plugin_abstain_diary
```  
打开 nonebot2 项目的 ```bot.py``` 文件, 在其中写入  
```nonebot.load_plugin('nonebot_plugin_abstain_diary')```  
当然，如果是默认nb-cli创建的nonebot2的话，在bot路径```pyproject.toml```的```[tool.nonebot]```的```plugins```中添加```nonebot_plugin_abstain_diary```即可  
pyproject.toml配置例如：  
``` 
[tool.nonebot]
plugin_dirs = ["src/plugins"]
plugins = ["nonebot_plugin_abstain_diary"]
``` 

### 更新版本
```
nb plugin update nonebot_plugin_abstain_diary
```

## 🔧 配置  
暂无，感觉没必要自定义了，先不开放。  

## 🎉 功能
戒色打卡。将用户期望戒色天数，用户群，用户QQ昵称，用户当前戒色天数等信息记录于本地bot的data/data.json文件中，方便用户对自己戒色信息的相关查询。  
*财能使人贪，色能使人嗜，名能使人矜，潜能使人倚，四患既都去，岂在浮尘里。*  

## 👉 命令

以下命令使用时记得加上自己的命令前缀哦~（一般为/）  

### 1、戒色帮助
命令结构：```/戒色帮助``` 或 ```/戒色说明``` 或 ```/戒色命令```  
例如：```/戒色帮助```  
bot返回内容：  
```
戒色命令如下(【】中的才是命令哦，记得加命令前缀)：
【戒色目标】【设置戒色目标】，后面追加戒色目标天数。例如：/戒色目标 30

【戒色】【戒色打卡】，每日打卡，请勿中断喵。例如：/戒色

【群戒色】【戒色情况】【群友戒色情况】，查看本群所有戒色情况。例如：/群戒色

财能使人贪，色能使人嗜，名能使人矜，潜能使人倚，四患既都去，岂在浮尘里。
```

### 2、戒色目标
命令结构：```/戒色目标``` 或 ```/设置戒色目标``` 后面追加 戒色目标天数  
例如：```/戒色目标 30```  
bot返回内容：  
```
戒色目标天数：30，设置成功！今天是打卡第一天，加油！你我都有美好的未来！
```

### 3、戒色
命令结构：```/戒色``` 或 ```/戒色打卡```  
例如：```/戒色```  
bot返回内容：  
```
戒色打卡成功！您已打卡1天！
```

### 4、群戒色
命令结构：```/群戒色``` 或 ```/戒色情况``` 或 ```/戒色情况```  
例如：```/群戒色```  
bot返回内容：  
```
群戒色信息

群昵称：只因
戒色目标天数：7
戒色打卡天数：1

群昵称：霓
戒色目标天数：1
戒色打卡天数：0

群昵称：太美
戒色目标天数：2
戒色打卡天数：1
```

### 4、放弃戒色
命令结构：```/放弃戒色``` 或 ```/取消戒色``` 或 ```/不戒色了```  
例如：```/放弃戒色```  
bot返回内容：  
```
戒色打卡已取消，您可以开冲啦！！！
```

## 📝 更新日志

<details>
<summary>展开/收起</summary>

### 0.0.1

- 插件初次发布  
  
### 0.0.2

- 修复首次运行数据文件加载失败bug
- 优化功能逻辑，设置目标即为开始打开第一天
- 优化文字描述

### 0.0.3

- 新增取消戒色功能
- 优化戒色目标天数校验
- 修复文件第二次加载时的数据异常bug

### 0.0.4

- 修复文件json数据加载bug
- 优化文档

### 0.0.5

- bug也太多了，绷
 

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