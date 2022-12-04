from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
import nonebot
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

data_json = [
    {
        "keyword": "pip",
        "msg": "更改pip国内镜像源的方法：https://blog.csdn.net/qq_40576301/article/details/125165926"
    },
    {
        "keyword": "nonebot",
        "msg": "windows从零手把手部署nonebot2：https://www.bilibili.com/video/BV1Ud4y1F7h3\n\
手把手从零搭建出属于自己的QQ机器人：https://www.cnblogs.com/daluobei/p/16495738.html"
    },
    {
        "keyword": "nb插件",
        "msg": "Nonebot2插件篇：https://space.bilibili.com/3709626/channel/collectiondetail?sid=850321"
    },
    {
        "keyword": "ddbot",
        "msg": "ddbot官方仓库：https://github.com/Sora233/DDBOT\n\
ddbot下载：https://github.com/Sora233/DDBOT/releases"
    },
    {
        "keyword": "游猴",
        "msg": "游猴官网：https://www.tampermonkey.net/index.php\n\
Greasy Fork插件网：https://greasyfork.org/zh-CN"
    },
    {
        "keyword": "gocq",
        "msg": "go-cqhttp文档：https://docs.go-cqhttp.org/"
    },
]

catch_str = on_keyword({'/小白 '})


@catch_str.handle()
async def _(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[4:]
    
    for i in range(len(data_json)):
        if content == data_json[i]["keyword"]:
            msg = '\n' + data_json[i]["msg"]
            break
        if i == len(data_json) - 1:
            msg = '\n果咩，没有此关键词的索引，请联系bot管理员添加~'

    await catch_str.finish(Message(f'{msg}'), at_sender=True)
