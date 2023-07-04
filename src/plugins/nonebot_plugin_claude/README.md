<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_claude
  
_✨ NoneBot 基于claude的聊天bot插件 ✨_
  
<a href="https://github.com/Ikaros-521/nonebot_plugin_claude/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Ikaros-521/nonebot_plugin_claude?color=%09%2300BFFF&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_claude/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Ikaros-521/nonebot_plugin_claude?color=Emerald%20green&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_claude/network">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/Ikaros-521/nonebot_plugin_claude?color=%2300BFFF&style=flat-square">
</a>
<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Ikaros-521/nonebot_plugin_claude.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_claude">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_claude.svg" alt="pypi">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</a>

</div>

适用于nonebot2 v11的基于claude的聊天bot插件  

## 🔧 开发环境
Nonebot2：2.0.0rc2  
python：3.10.8  
操作系统：Windows10（Linux兼容性问题不大）  
编辑器：VS Code  

## 💿 安装
环境依赖`slack_sdk`库   

### 1. nb-cli安装（暂不发布，无法使用）
在你bot工程的文件夹下，运行cmd（运行路径要对啊），执行nb命令安装插件，插件配置会自动添加至配置文件  
```
nb plugin install nonebot_plugin_claude
```

### 2. 本地安装
先安装下 `slack_sdk`  
```
pip install slack_sdk
```
将项目clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的`src/plugins`），然后把`nonebot_plugin_claude`文件夹里的内容拷贝至上一级目录即可。  
clone命令参考（得先装`git`，懂的都懂）：
```
git clone https://github.com/Ikaros-521/nonebot_plugin_claude.git
``` 
也可以直接下载压缩包到插件目录解压，然后同样提取`nonebot_plugin_claude`至上一级目录。  
目录结构： ```你的bot/src/plugins/nonebot_plugin_claude/__init__.py```  


### 3. pip安装（暂不发布，无法使用）
```
pip install nonebot_plugin_claude
```  
打开 nonebot2 项目的 ```bot.py``` 文件, 在其中写入  
```nonebot.load_plugin('nonebot_plugin_claude')```  
当然，如果是默认nb-cli创建的nonebot2的话，在bot路径```pyproject.toml```的```[tool.nonebot]```的```plugins```中添加```nonebot_plugin_claude```即可  
pyproject.toml配置例如：  
``` 
[tool.nonebot]
plugin_dirs = ["src/plugins"]
plugins = ["nonebot_plugin_claude"]
``` 

### 更新版本（暂不可用）
```
nb plugin update nonebot_plugin_claude
```

## 🔧 配置  

### env配置
```
# nonebot_plugin_claude 官方oauth token
claude_api_key="xoxp-1111-1111-1111-123abc"
claude_user_id="U123456789"
```
|       配置项        | 必填 | 默认值  |    说明      |
|:----------------:|:----:|:----:|:----------------------------:|
| `claude_api_key` | 是 | `""` | 注册官方账号申请APP等，开通token（开通方式参考：https://github.com/bincooo/claude-api#readme） |
| `claude_user_id` | 是 | `""` | 在slack聊天区选中claude查看ID信息（具体参考：https://github.com/bincooo/claude-api#readme） |
| `claude_proxy` | 否 | `None` | 代理地址，非必填(例如：claude_proxy="http://127.0.0.1:10809") |

### token和user_id获取方式
参考：[https://github.com/bincooo/claude-api#readme](https://github.com/bincooo/claude-api#readme)

## 🎉 功能
调用Slack中claude的API，实现大语言模型聊天。   

## 👉 命令

### /claude 或 /cld

命令格式: /claude <提问内容> 
例如：  
```
/claude 你好
/cld 请使用python实现一个汉诺塔
```
bot返回内容：  
![](docs/result.png)

## ⚙ 拓展
修改`__init__.py`中的`catch_str`等来自定义命令触发关键词。     

## 📝 更新日志

<details>
<summary>展开/收起</summary>

### 0.0.1

- 插件初次发布

### 0.0.2

- 新增代理配置

</details>

## 致谢

- [claude-api](https://github.com/bincooo/claude-api) - 使用注册讲解
- [Claude_In_Slack_API](https://github.com/jasonthewhale/Claude_In_Slack_API) - 源码参考
- [api.slack.com](https://api.slack.com/) - 官方API   

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