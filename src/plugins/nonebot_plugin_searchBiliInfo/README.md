<div align="center">

# nonebot_plugin_searchBiliInfo
  
_✨ NoneBot b站用户直播号、粉丝、舰团数查询插件 ✨_
  

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/tkgs0/nonebot-plugin-antiinsult.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_searchBiliInfo">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_searchBiliInfo.svg" alt="pypi">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</a>

</div>

适用于nonebot2 v11的b站用户粉丝、舰团信息查询插件（微调源码可以兼容其他版本）   
调用的相关API均为b站官方接口  

## 🔧 开发环境
Nonebot2：2.0.0b5  
python：3.8.13  
操作系统：Windows10（CentOS7下正常运行，Linux兼容性问题不大）  
编辑器：pycharm  

## 💿 安装
环境依赖requests库，记得安装下 `pip install requests`  
### 本地安装
将文件夹clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的src/plugins）即可，也可以直接下载压缩包到插件目录解压。  
目录结构： ```你的bot/src/plugins/nonebot_plugin_searchBiliInfo```  
```git clone https://github.com/Ikaros-521/nonebot_plugin_searchBiliInfo.git```  
### pip安装
```pip install nonebot_plugin_searchBiliInfo```  
打开 nonebot2 项目的 ```bot.py``` 文件, 在其中写入  
```nonebot.load_plugin('nonebot_plugin_antiinsult')```  
当然，如果是默认配置的nonebot2的话，在bot路径```pyproject.toml```的```[tool.nonebot]```的```plugins```中添加```nonebot_plugin_searchBiliInfo```即可


## 🎉 功能
通过uid或设定好的短语或b站接口搜索查询指定b站用户的粉丝、舰团信息。

## 👉 命令
命令结构：```/查 用户uid或设定好的昵称```  
例如：```/查 用户uid 或 设定好的昵称 或 关键词```(昵称设定修改查看文档下方 拓展)
bot返回内容：
```
用户名：bishi
UID：1
房间号：553241
粉丝数：161841
舰团数：0
```
## ⚙️ 拓展
启用关键词搜索，需要修改__init__.py的header1的cookie，获取自己的cookie，填入。

命令修改：修改data.py，在文件头部追加你需要定义的用户的json串，注意json格式！！！

返回内容格式修改：修改__init__.py的75行部分，msg变量的内容  

## 项目打包

```
参考 https://www.cnblogs.com/danhuai/p/14915042.html
创建setup.py文件 填写相关信息

# 4.1、可以先升级打包工具
pip install --upgrade setuptools wheel twine

# 4.2、打包
python setup.py sdist bdist_wheel

# 4.3、可以先检查一下包
twine check dist/*

# 4.4、上传包到pypi（需输入用户名、密码）
twine upload dist/*
```

## 📝 更新日志

<details>
<summary>展开/收起</summary>

### 0.0.1

- 插件初次发布

### 0.1.0

- 更新基于vtbs.moe的主播数据，添加关键词搜索功能

</details>

