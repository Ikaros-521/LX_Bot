# LX_Bot
基于nonebot2开发的个人bot，配合gocqhttp使用，持续更新中

nonebot2版本：2.0.0b5
python版本：3.8.5  
安装nonebot2脚手架 `pip install nb-cli`  
随便创建个v11的项目会补装一些依赖（ps：空格是选中，不要建错了） `nb create`  
补装 aiocqhttp  `pip install aiocqhttp`  

以下插件自行选择（有些插件需要一些配置项，请在.env.prod里面补充完整）  
- haruka_bot推送b站信息`nb plugin install haruka_bot`  
- nonebot_plugin_status查看服务器运行信息（win不适用）`nb plugin install nonebot_plugin_status`  
- 短句回复插件`nb plugin install nonebot_plugin_abbrreply`  
- bilibili 视频、番剧解析插件`nb plugin install nonebot_plugin_analysis_bilibili`  
- 简单撤回插件，让机器人撤回 自己发出的消息`nb plugin install nonebot_plugin_withdraw`  
- 点歌插件 支持 qq、网易云、酷我、酷狗、咪咕、b站音频区`nb plugin install nonebot_plugin_simplemusic`  
- 制作头像相关的表情包插件（第一次运行报错，重启运行成功）`nb plugin install nonebot_plugin_petpet`  
- 做表情包插件，下载可能出错，参考https://github.com/noneplugin/nonebot-plugin-memes ，手动添加图片资源等 `nb plugin install nonebot_plugin_memes`  
- 获取群聊天消息的词云图`nb plugin install nonebot_plugin_wordcloud`  
- 提取b站视频封面`nb plugin install nonebot-plugin-bilicover`  
- 百度翻译插件`nb plugin install nonebot_plugin_baidutranslate`  
- 非侵入式插件管理器`nb plugin install nonebot_plugin_manager`  
- 搜索引擎插件`nb plugin install nonebot_plugin_giyf`  
- 轮盘禁言小游戏(功能需要给bot设置为管理员，命令参考：https://github.com/KarisAya/nonebot_plugin_russian_ban) `nb plugin install nonebot_plugin_russian_ban`  
- 和Bot说早晚安，记录睡眠时间，培养良好作息 `nb plugin install nonebot_plugin_morning`  
- 娶群友插件 `nb plugin install nonebot_plugin_groupmate_waifu`  
- 吃喝什么帮你选插件 `nb plugin install nonebot_plugin_what2eat`  
- 塔罗牌占卜插件 `nb plugin install nonebot_plugin_tarot`  
- 获取Epic限免游戏资讯插件 `nb plugin install nonebot_plugin_epicfree`  
- 使用Kyomotoi/AnimeThesaurus的回复（文i）插件 `nb plugin install nonebot_plugin_kawaii_robot`
- 帮你搜索 bangumi上的条目，并且根据你选择的搜索结果给你发送该条目的侧边简介栏和收藏盒 `nb plugin install nonebot-plugin-bangumi-search`  
- 日韩中 VITS 模型拟声 `nb plugin install nonebot_plugin_moegoe`  
- 话痨排行榜插件（win可以使用） `nb plugin install nonebot-plugin-dialectlist`  
- 展示原神游戏每日材料数据 `nb plugin install nonebot-plugin-gsmaterial`  
- 识别二维码插件 `nb plugin install nonebot-plugin-qrcode`  
- emoji合成器 `nb plugin install nonebot_plugin_emojimix`  
- 用于抽象话等文本生成 `nb plugin install nonebot_plugin_oddtext`  
- 图片合成库（支持md，html，文字等）`nb plugin install nonebot-plugin-htmlrender`  
- 图片超分辨率放大`nonebot-plugin-super-resolution`  
- 对三次元图像动漫化`nonebot-plugin-cartoon`  
- 投胎模拟器`nonebot-plugin-reborn`  
- 随个群友当幸运观众`nonebot-plugin-person`  
- 展示原神游戏内角色展柜数据`nb plugin install nonebot-plugin-gspanel`  
- 明日方舟小工具箱插件`nb plugin install nonebot_plugin_arktools`  
- 磁力搜索插件`nb plugin install nonebot_plugin_BitTorrent`  

qq发送 `/help` 呼出帮助手册，`/帮助`呼出haruka的帮助  
在线帮助文档：https://docs.qq.com/sheet/DWURzcWhWR2tSTE10  

gocqhttp核心配置如下：
```
# 连接服务列表
servers:
  # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
  #- http: # http 通信
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器
  # 反向WS设置
  - ws-reverse:
      # 反向WS Universal 地址
      # 注意 设置了此项地址后下面两项将会被忽略
      universal: ws://127.0.0.1:12345/ws/
      # 反向WS API 地址
      api: ws://your_websocket_api.server
      # 反向WS Event 地址
      event: ws://your_websocket_event.server
      # 重连间隔 单位毫秒
      reconnect-interval: 3000
      middlewares:
        <<: *default # 引用默认中间件

```

## How to start

1. generate project using `nb create` .
2. create your plugin using `nb plugin create` .
3. writing your plugins under `src/plugins` folder.
4. run your bot using `nb run` .

## Documentation

See [Docs](https://v2.nonebot.dev/)
