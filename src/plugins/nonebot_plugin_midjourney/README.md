<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_midjourney
  
_✨ NoneBot 基于midjourney的绘图插件 ✨_
  
<a href="https://github.com/Ikaros-521/nonebot_plugin_midjourney/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Ikaros-521/nonebot_plugin_midjourney?color=%09%2300BFFF&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_midjourney/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Ikaros-521/nonebot_plugin_midjourney?color=Emerald%20green&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_midjourney/network">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/Ikaros-521/nonebot_plugin_midjourney?color=%2300BFFF&style=flat-square">
</a>
<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Ikaros-521/nonebot_plugin_midjourney.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_midjourney">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_midjourney.svg" alt="pypi">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</a>

</div>

适用于nonebot2 v11的基于midjourney的绘图插件  

## 🔧 开发环境
Nonebot2：2.0.0rc2  
python：3.10.8  
操作系统：Windows10（Linux兼容性问题不大）  
编辑器：VS Code  

## 💿 安装
环境依赖`pandas aiohttp`库   

### 1. nb-cli安装（暂不发布，无法使用）
在你bot工程的文件夹下，运行cmd（运行路径要对啊），执行nb命令安装插件，插件配置会自动添加至配置文件  
```
nb plugin install nonebot_plugin_midjourney
```

### 2. 本地安装
先安装下 `pandas aiohttp`  
```
pip install pandas aiohttp
```
将项目clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的`src/plugins`），然后把`nonebot_plugin_midjourney`文件夹里的内容拷贝至上一级目录即可。  
clone命令参考（得先装`git`，懂的都懂）：
```
git clone https://github.com/Ikaros-521/nonebot_plugin_midjourney.git
``` 
也可以直接下载压缩包到插件目录解压，然后同样提取`nonebot_plugin_midjourney`至上一级目录。  
目录结构： ```你的bot/src/plugins/nonebot_plugin_midjourney/__init__.py```  


### 3. pip安装（暂不发布，无法使用）
```
pip install nonebot_plugin_midjourney
```  
打开 nonebot2 项目的 ```bot.py``` 文件, 在其中写入  
```nonebot.load_plugin('nonebot_plugin_midjourney')```  
当然，如果是默认nb-cli创建的nonebot2的话，在bot路径```pyproject.toml```的```[tool.nonebot]```的```plugins```中添加```nonebot_plugin_midjourney```即可  
pyproject.toml配置例如：  
``` 
[tool.nonebot]
plugin_dirs = ["src/plugins"]
plugins = ["nonebot_plugin_midjourney"]
``` 

### 更新版本（暂不可用）
```
nb plugin update nonebot_plugin_midjourney
```

## 🔧 配置  

### config配置
配置文件在第一次运行时会自动生成（失败的话，可以手动创建），位于`项目根目录/data/nonebot_plugin_midjourney/config.json`  
配置项源自discord自建服务器请求Midjourney Bot时的请求包中。  
参考：[https://github.com/Ikaros-521/Midjourney_api](https://github.com/Ikaros-521/Midjourney_api)  
```
{
    "channelid": "1111111111111111111",
    "authorization": "aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbb.111111111111_666_222222222222222222222",
    "application_id": "111111111111111111",
    "guild_id": "1111111111111111111",
    "session_id": "11111111111111111111111111111111",
    "version": "1111111111111111111",
    "id": "111111111111111111",
    "flags": "--v 5",
    "proxy": "http://127.0.0.1:10809",
    "timeout": 120
}
```

1. 创建Discord帐户并创建您的服务器（说明在此处：https://discord.com/blog/starting-your-first-discord-server）
2. 加入midjourney官方频道[https://discord.gg/midjourney](https://discord.gg/midjourney)
3. 创建Midjourney帐户并邀请Midjourney机器人到您的服务器（说明在此处：https://docs.midjourney.com/docs/invite-the-bot）
4. 确保从您的服务器进行生成操作
5. 在浏览器中登录Discord，打开您的服务器的文本频道，点击右上角的三个点，然后选择更多工具，再选择 "开发者工具"（直接键盘按F12）。
选择 "网络" 选项卡，您将看到页面的所有网络活动。
1. 现在在您的文本频道中输入任何提示进行生成，按Enter键发送提示消息后，您将在网络活动中看到一个名为“interaction”的新行。
点击它并选择"Payload"（负载）选项卡，您将看到 payload_json - 这就是我们需要的请求相关的参数！
复制channelid、authorization(请求头中获取)、application_id、guild_id、session_id、version和id值，稍后我们会用到它们。
1. 克隆这个repo。
2. 打开“sender_params.json”文件并将第5段中的所有值放入其中。还要填写“flags”字段以指定提示的特殊标志。  
ps：如果你想要使用代理访问，请修改配置文件中的`proxy`为`true`，并在下面`http_proxy`和`https_proxy`的配置你的代理地址。  
1. 现在，您已准备好运行文件：
要启动接收器脚本，请打开终端并输入：
`python receiver.py --params sender_params.json --local_path "./download"`
此脚本将向您显示所有的生成进度，并在图像准备就绪时立即下载图像到`--local_path`设置的路径。

要发送生成提示`--prompt`后就是关键词字符串，请在另一个终端中打开并输入：
`python sender.py --params sender_params.json --prompt "your prompt here"`
9. 尽情享受吧 :)

请注意控制并行请求的数量 - 对于正常和最快的工作，它不应该超过3（在基础和标准计划中），在专业计划中为12。

## 🎉 功能
调用Discord中midjourney的接口，实现命令发送和图片捕获。   

## 👉 命令

### /midj 或 /mj

命令格式: /mj <prompt> 
例如：  
```
/mj a girl
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

</details>

## 致谢

- [Midjourney_api](https://github.com/George-iam/Midjourney_api) - 源码参考   

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