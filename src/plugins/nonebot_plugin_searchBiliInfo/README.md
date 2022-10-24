# nonebot_plugin_searchBiliInfo
适用于nonebot2 v11的b站用户粉丝、舰团信息查询插件（微调源码可以兼容其他版本）   
调用的相关API均为b站官方接口  

## 安装
环境依赖requests库，记得安装下 `pip install requests`  
将文件夹clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的src/plugins）即可，也可以直接下载压缩包到插件目录解压。  
目录结构： 你的bot/src/plugins/nonebot_plugin_searchBiliInfo  

## 功能
通过uid或设定好的短语查询指定b站用户的粉丝、舰团信息。

## 命令
命令结构：```/查 用户uid或设定好的昵称```  
例如：```/查 1```  ```/查 lulu``` (昵称设定修改查看文档下方 拓展)  
bot返回内容：
```
用户名：bishi
UID：1
房间号：553241
粉丝数：161841
舰团数：0
```
## 拓展
命令修改：修改__init__.py的8行部分，catch_str变量的内容  

昵称设定：修改__init__.py的19,20行部分，name和uid这2个数组，按对应关系填入（索引要一一对应）  

返回内容格式修改：修改__init__.py的42行部分，msg变量的内容  