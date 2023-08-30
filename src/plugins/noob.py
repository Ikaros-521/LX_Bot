from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.params import CommandArg
# import nonebot
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

data_json = [
    {
        "keyword": "帮助",
        "msg": "关键词：pip、nonebot、nb插件、ddbot、油猴、gocq、红包插件、ssh"
    },
    {
        "keyword": "pip",
        "msg": "更改pip国内镜像源的方法：https://blog.csdn.net/qq_40576301/article/details/125165926\n\
https://blog.csdn.net/wejack/article/details/126228290"
    },
    {
        "keyword": "nonebot",
        "msg": "官方仓库：https://github.com/nonebot/nonebot2\n\
windows从零手把手部署nonebot2：https://www.bilibili.com/video/BV1Ud4y1F7h3\n\
手把手从零搭建出属于自己的QQ机器人：https://www.cnblogs.com/daluobei/p/16495738.html"
    },
    {
        "keyword": "nb插件",
        "msg": "官方插件商店：https://v2.nonebot.dev/store\n\
Nonebot2插件篇：https://space.bilibili.com/3709626/channel/collectiondetail?sid=850321"
    },
    {
        "keyword": "ddbot",
        "msg": "ddbot官方仓库：https://github.com/Sora233/DDBOT\n\
ddbot下载：https://github.com/Sora233/DDBOT/releases"
    },
    {
        "keyword": "油猴",
        "msg": "油猴官网：https://www.tampermonkey.net/index.php\n\
Greasy Fork插件网：https://greasyfork.org/zh-CN"
    },
    {
        "keyword": "gocq",
        "msg": "go-cqhttp文档：https://docs.go-cqhttp.org/\n\
官方仓库：https://github.com/Mrs4s/go-cqhttp\n\
软件下载：https://github.com/Mrs4s/go-cqhttp/releases（win一般下amd64，Linux看架构选择）"
    },
    {
        "keyword": "红包插件",
        "msg": "B站直播自动抢红包：https://greasyfork.org/zh-CN/scripts/439169\n\
自动检索红包直播间并跳转：https://greasyfork.org/zh-CN/scripts/447595\n\
不影响抽红包的多余内容删除：https://greasyfork.org/zh-CN/scripts/447830"
    },
    {
        "keyword": "ssh",
        "msg": "ubuntu root用户ssh登录：https://blog.csdn.net/yao51011010/article/details/128530501"
    },
    {
        "keyword": "ai",
        "msg": "AI收集表：https://docs.qq.com/sheet/DWXBzaERNaXRpT1Rj"
    },
    {
        "keyword": "vits",
        "msg": "VITS-fast-fine-tuning官方仓库：https://github.com/Plachtaa/VITS-fast-fine-tuning\n\
个人提供的已训练好的模型：https://github.com/Ikaros-521/VITS-fast-fine-tuning/releases\n\
视频教程：https://www.bilibili.com/video/BV1Lm4y1r7Pi"
    },
    {
        "keyword": "so-vits",
        "msg": "so-vits-svc官方仓库：https://github.com/svc-develop-team/so-vits-svc\n\
个人提供的已训练好的模型：https://github.com/Ikaros-521/so-vits-svc/releases\n\
视频教程：https://www.bilibili.com/video/BV1k24y1F7Us"
    },
    {
        "keyword": "ai vtb",
        "msg": "视频合集：https://space.bilibili.com/3709626/channel/collectiondetail?sid=1422512\n\
相关整合/半整合包发布 https://github.com/Ikaros-521/AI-Vtuber/releases/\n\
夸克网盘：https://pan.quark.cn/s/e6755e65dc05\n\
阿里云盘：https://www.aliyundrive.com/s/JRWomhcpeN9"
    }
]

catch_str = on_command('小白')

@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    
    for i in range(len(data_json)):
        if content == data_json[i]["keyword"]:
            msg = '\n' + data_json[i]["msg"]
            break
        if i == len(data_json) - 1:
            msg = '\n果咩，没有此关键词的索引，请联系bot管理员添加~'

    await catch_str.finish(Message(f'{msg}'), at_sender=True)
