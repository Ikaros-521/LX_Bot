<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_random_ban
  
_✨ NoneBot 随机禁言插件 ✨_
  
<a href="https://github.com/Ikaros-521/nonebot_plugin_random_ban/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Ikaros-521/nonebot_plugin_random_ban?color=%09%2300BFFF&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_random_ban/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Ikaros-521/nonebot_plugin_random_ban?color=Emerald%20green&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_random_ban/network">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/Ikaros-521/nonebot_plugin_random_ban?color=%2300BFFF&style=flat-square">
</a>
<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Ikaros-521/nonebot_plugin_random_ban.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_random_ban">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_random_ban.svg" alt="pypi">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</a>

</div>

适用于nonebot2 v11的随机禁言一名群员或自己n分钟 插件      
注意：需要给bot管理员才能使用。  

## 🔧 开发环境
Nonebot2：2.0.0b5  
python：3.8.13  
操作系统：Windows10（Linux兼容性问题不大）  
编辑器：pycharm  

## 💿 安装

### 1. nb-cli安装（推荐）

在你bot工程的文件夹下，运行cmd（运行路径要对啊），执行nb命令安装插件，插件配置会自动添加至配置文件  
```
nb plugin install nonebot_plugin_random_ban
```

### 2. 本地安装

将项目clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的`src/plugins`），然后把`nonebot_plugin_random_ban`文件夹里的内容拷贝至上一级目录即可。  
clone命令参考（得先装`git`，懂的都懂）：
```
git clone https://github.com/Ikaros-521/nonebot_plugin_random_ban.git
``` 
也可以直接下载压缩包到插件目录解压，然后同样提取`nonebot_plugin_random_ban`至上一级目录。  
目录结构： ```你的bot/src/plugins/nonebot_plugin_random_ban/__init__.py```  


### 3. pip安装

```
pip install nonebot_plugin_random_ban
```  
打开 nonebot2 项目的 ```bot.py``` 文件, 在其中写入  
```nonebot.load_plugin('nonebot_plugin_random_ban')```  
当然，如果是默认nb-cli创建的nonebot2的话，在bot路径```pyproject.toml```的```[tool.nonebot]```的```plugins```中添加```nonebot_plugin_random_ban```即可  
pyproject.toml配置例如：  
``` 
[tool.nonebot]
plugin_dirs = ["src/plugins"]
plugins = ["nonebot_plugin_random_ban"]
``` 

### 更新版本
```
nb plugin update nonebot_plugin_random_ban
```

## 🔧 配置

### env配置
```
# nonebot_plugin_random_ban
# 任何人都可以使用 随机禁言，开启后将会迎来至暗时刻
anyone_can_random_ban = []
```
若某群想长期启动`至暗时刻`，配置参考：  
```
# nonebot_plugin_random_ban
# 任何人都可以使用 随机禁言，开启后将会迎来至暗时刻
anyone_can_random_ban = [123456, 114514]
```
|       配置项      | 必填 | 默认值 |             说明            |
|:----------------:|:----:|:----:|:----------------------------:|
| `nonebot_plugin_random_ban` | 否 | `[]` | 数组内配置开启`至暗时刻`的群号即可 |



## 🎉 功能
随机禁言一名群员或自己n分钟（n通过传入数字然后随机实现），简单粗暴。可以`开启至暗时刻`，就是所有人可以使用`随禁`命令，刺激。    

## 👉 命令

### 随机禁言 或 随禁
命令结构：```/随机禁言 [最大禁言时间]``` 或 ```/随禁 [最大禁言时间]```  （最大禁言时间不填默认60分钟内的随机）  
例如：```/随机禁言``` 或 ```/随禁 10``` 或 ```/随禁 10分``` 或 ```/随禁 10时``` 或 ```/随禁 10天```   
bot返回内容：  
```
恭喜幸运儿:xxx 获得6分钟的禁言服务
```

### 口球 或 禁我
命令结构：```/口球 [最大禁言时间]``` 或 ```/禁我 [最大禁言时间]```  （最大禁言时间不填默认60分钟内的随机）  
例如：```/口球``` 或 ```/禁我 10``` 或 ```/禁我 10分``` 或 ```/口球 10时``` 或 ```/口球 10天```   
bot返回内容：  
```
恭喜您获得6分钟的禁言服务
```

### 开启至暗时刻
命令结构：```/开启至暗时刻``` 或 ```/至暗时刻启动``` 或 ```/至暗时刻开启```  或 ```/启动至暗时刻```  
例如：```/开启至暗时刻```  
说明：至暗时刻就是所有人可以使用 `/随禁` 命令，将是一片腥风血雨。  
bot返回内容：  
```
本群开启 至暗时刻成功，开始狩猎吧！
```

### 关闭至暗时刻
命令结构：```/关闭至暗时刻``` 或 ```/至暗时刻关闭``` 或 ```/停止至暗时刻```  或 ```/至暗时刻停止```  
例如：```/关闭至暗时刻```  
bot返回内容：  
```
本群已关闭 至暗时刻，世界恢复和平。
```

![](docs/result.jpg)

## ⚙ 拓展
自行修改源码喵~


## 📝 更新日志

<details>
<summary>展开/收起</summary>

### 0.0.1

- 插件初次发布  

### 0.0.2

- 补充插件元信息
- 优化文档

### 0.0.3

- 新增命令 口球 或 禁我，自己禁自己

### 0.0.4

- 优化文档

### 0.0.5

- 新增可以开启任何人都使用随机禁言的配置项

### 0.1.0

- 新增 至暗时刻，就是所有人可以使用`随禁`命令，刺激。

### 0.2.0

- 新增 传参的单位兼容，分、分钟、时、小时、天。
- 修改 艾特 为 回复的形式。
- 优化代码。

### 0.2.1

- 修复 传参只匹配数字不匹配单位的bug
- 修复 传入禁言时长大于30天的bug

</details>

