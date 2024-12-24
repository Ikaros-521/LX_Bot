<div align="center">
  <a href="#">
    <img src="https://raw.githubusercontent.com/LuoXi-Project/LX_Project_Template/refs/heads/main/ui/logo.png" width="240" height="240" alt="点我跳转文档">
  </a>
</div>

<div align="center">

# ✨ 洛曦 Bot  ✨

[![][python]][python]
[![][github-release-shield]][github-release-link]
[![][github-stars-shield]][github-stars-link]
[![][github-forks-shield]][github-forks-link]
[![][github-issues-shield]][github-issues-link]  
[![][github-contributors-shield]][github-contributors-link]
[![][github-license-shield]][github-license-link]

</div>

基于[nonebot2](https://v2.nonebot.dev/)开发的个人bot，配合[go-cqhttp](https://docs.go-cqhttp.org/)、[NapCatQQ](https://github.com/NapNeko/NapCatQQ)、NTQQ+[LLOneBot](https://github.com/LLOneBot/LLOneBot)使用，持续更新中

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## [目录](https://github.com/thlorenz/doctoc)

- [LX\_Bot](#lx_bot)
  - [目录](#目录)
  - [QQ客户端](#qq客户端)
  - [环境和nb安装](#环境和nb安装)
  - [插件安装和卸载](#插件安装和卸载)
  - [帮助说明](#帮助说明)
  - [go-cqhttp配置](#go-cqhttp配置)
  - [How to start](#how-to-start)
  - [Documentation](#documentation)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## QQ客户端

推荐：[https://github.com/NapNeko/NapCatQQ](https://github.com/NapNeko/NapCatQQ)  
webui地址：http://127.0.0.1:6099/webui  
反向WS地址：ws://127.0.0.1:54321/onebot/v11/ws  
Linux下webui.json路径（token获取）：/opt/QQ/resources/app/app_launcher/napcat/config  


配合NTQQ使用：[https://github.com/LLOneBot/LLOneBot](https://github.com/LLOneBot/LLOneBot)

## 环境和nb安装
nonebot2版本：2.0.0rc2
python版本：3.10  

打开cmd，安装nonebot2脚手架 `pip install nb-cli`  
随便创建个v11的项目会补装一些依赖（ps：空格是选中，不要建错了） `nb create`  
补装 aiocqhttp  `pip install aiocqhttp`  

克隆本项目到本地路径 `git clone https://github.com/Ikaros-521/LX_Bot.git`  
进入项目文件夹 `cd LX_Bot`  
由于项目内置了我自己写的一些插件，这些插件有相关库的依赖，如果想要使用需要补装库如下（注意用nb装的时候请在bot的根目录运行）：  
```
pip install aiohttp
nb plugin install nonebot_plugin_imageutils
nb plugin install nonebot_plugin_htmlrender
pip install lxml

```

ps: 由于`2d_pixiv_img2.py`，使用了opencv做了幻影坦克，所以需要装`pip install opencv-python`，如果对此插件没有需求，可以删除此插件。  

## 插件安装和卸载
安装以下插件时，请在`bot`的根目录运行，因为`nb`命令会自动添加插件至`pyproject.toml`配置文件。  
卸载就把`install`换成`uninstall`就可以了。  
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
- 疫情小助手 支持查地区 风险地区 境外输入等`nb plugin install nonebot-plugin-covid-19-by`  
- 在线运行代码插件`nb plugin install nonebot-plugin-code`  
- 用于订阅 RSS 并实时以 QQ消息推送`nb plugin install ELF_RSS2`  
- 掷骰子插件`nb plugin install nonebot_plugin_roll`  
- 今日运势插件`nb plugin install nonebot_plugin_fortune`  
- 游戏王卡查插件`nb plugin install nonebot_plugin_ygo`  
- 和风天气`nb plugin install nonebot-plugin-heweather`  
- 工作性价比计算器`nb plugin install nonebot_plugin_workscore`  
- 有提醒功能的记事本`nb plugin install nonebot_plugin_note`  
- ChatGPT AI 对话`nb plugin install nonebot-plugin-chatgpt`  
- 插件菜单插件(需要手动加载插件)`pip install nonebot-plugin-PicMenu`
- 随机唐可可`nb plugin install nonebot-plugin-randomtkk`  
- 不要复读`nb plugin install nonebot_plugin_no_repeat`  
- 免费版NovelAI生图插件`nb plugin install nonebot-plugin-zyk-novelai`  
- 内置数据库的setu插件`nb plugin install nonebot-plugin-setu4`  
- openAI GPT3插件`nb plugin install nonebot-plugin-gpt3`  

## 帮助说明
qq发送 `/help` 呼出帮助手册，`/帮助`呼出haruka的帮助  
在线帮助文档：https://docs.qq.com/sheet/DWURzcWhWR2tSTE10  

## go-cqhttp配置
go-cqhttp核心配置如下：  
universal不对的话，可以改成`ws://127.0.0.1:54321/ws/` 试试  
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
      universal: ws://127.0.0.1:54321/onebot/v11/ws/
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



[python]: https://img.shields.io/badge/python-3.10+-blue.svg?labelColor=black
[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-black?style=flat-square
[github-action-release-link]: https://github.com/actions/workflows/Ikaros-521/LX_Bot/release.yml
[github-action-release-shield]: https://img.shields.io/github/actions/workflow/status/Ikaros-521/LX_Bot/release.yml?label=release&labelColor=black&logo=githubactions&logoColor=white&style=flat-square
[github-action-test-link]: https://github.com/actions/workflows/Ikaros-521/LX_Bot/test.yml
[github-action-test-shield]: https://img.shields.io/github/actions/workflow/status/Ikaros-521/LX_Bot/test.yml?label=test&labelColor=black&logo=githubactions&logoColor=white&style=flat-square
[github-codespace-link]: https://codespaces.new/Ikaros-521/LX_Bot
[github-codespace-shield]: https://github.com/codespaces/badge.svg
[github-contributors-link]: https://github.com/Ikaros-521/LX_Bot/graphs/contributors
[github-contributors-shield]: https://img.shields.io/github/contributors/Ikaros-521/LX_Bot?color=c4f042&labelColor=black&style=flat-square
[github-forks-link]: https://github.com/Ikaros-521/LX_Bot/network/members
[github-forks-shield]: https://img.shields.io/github/forks/Ikaros-521/LX_Bot?color=8ae8ff&labelColor=black&style=flat-square
[github-issues-link]: https://github.com/Ikaros-521/LX_Bot/issues
[github-issues-shield]: https://img.shields.io/github/issues/Ikaros-521/LX_Bot?color=ff80eb&labelColor=black&style=flat-square
[github-license-link]: https://github.com/Ikaros-521/LX_Bot/blob/main/LICENSE
[github-license-shield]: https://img.shields.io/github/license/Ikaros-521/LX_Bot?color=white&labelColor=black&style=flat-square
[github-release-link]: https://github.com/Ikaros-521/LX_Bot/releases
[github-release-shield]: https://img.shields.io/github/v/release/Ikaros-521/LX_Bot?color=369eff&labelColor=black&logo=github&style=flat-square
[github-releasedate-link]: https://github.com/Ikaros-521/LX_Bot/releases
[github-releasedate-shield]: https://img.shields.io/github/release-date/Ikaros-521/LX_Bot?labelColor=black&style=flat-square
[github-stars-link]: https://github.com/Ikaros-521/LX_Bot/network/stargazers
[github-stars-shield]: https://img.shields.io/github/stars/Ikaros-521/LX_Bot?color=ffcb47&labelColor=black&style=flat-square
[pr-welcome-link]: https://github.com/Ikaros-521/LX_Bot/pulls
[pr-welcome-shield]: https://img.shields.io/badge/%F0%9F%A4%AF%20PR%20WELCOME-%E2%86%92-ffcb47?labelColor=black&style=for-the-badge
[profile-link]: https://github.com/LuoXi-Project

