<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_listener
  
_✨ 基于nonebot2的监听者魔改版  ✨_

</div>


## 简介

可以监听指定群、指定对象、指定内容，进行消息百度翻译  

## 配置

.env.xx的配置  
```
# 以下均为百度翻译配置，见 https://fanyi-api.baidu.com/doc/21
appid = "xxx"  # 你的 APP ID，在百度翻译的开发者中心里可以找到
key = "xxx"    # 你的密钥，在百度翻译的开发者中心里可以找到
salt = "xxx"   # 随机字符串
```

## 使用
将项目下载解压到bot的src/plugins目录  
填写config2.py 90行左右的内容即可（具体填写方式参考注释）  

魔改后，只需要修改`listen_groups`、`listen_users`即可，`send_groups`已失效  
`listen_groups`为需要监听的群号，`listen_users`为需要监听的QQ号  
`listen_type`是需要监听的消息类型，默认是 纯文字 + 回复的消息  
