import aiohttp, json
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.params import CommandArg


catch_str = on_command('z-lib', aliases={"搜书"})


@catch_str.handle()
async def send_msg(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    # 信息源自 群聊或私聊
    msg_from = "group"
    if isinstance(event, GroupMessageEvent):
        # nonebot.logger.info("群聊")
        group = str(event.group_id)
    else:
        # nonebot.logger.info("私聊")
        private = event.get_user_id()
        msg_from = "private"

    content = msg.extract_plain_text().strip()

    data = await get_data(content)

    if data == "error":
        msg = '命令错误，命令格式：/搜书 [书名]'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    data_json = json.loads(data)

    msgList = []
    msgList.extend(
        [
            MessageSegment.node_custom(
                user_id=10000,
                nickname="bot",
                content=Message(MessageSegment.text(json.dumps(data_json, indent=2, ensure_ascii=False))),
            ),
            MessageSegment.node_custom(
                user_id=10000,
                nickname="bot",
                content=Message(MessageSegment.text('下载地址：https://gateway.pinata.cloud//ipfs/ 链接后面追加书的ipfs_cid即可。')),
            )
        ]
    ) 

    try:
        # 判断消息类型
        if msg_from == "group":
            await bot.send_group_forward_msg(group_id=group, messages=msgList)
        else:
            await bot.send_private_forward_msg(user_id=private, messages=msgList)
    except:
        msg = '果咩，数据发送失败喵~请查看源码和日志定位问题原因'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data(content):
    limit = 5
    title = ""

    title = content

    # if len(arr) > 2 or len(arr) == 0:
    #     return "error"
    # elif len(arr) == 2:
    #     title = content.split()[0]
    #     limit = int(content.split()[1])
    # else:
    #     title = content.split()[0]

    API_URL = 'https://zlib.cydiar.com/search?limit=' + str(limit) +\
        '&query=title:"' + title + '"'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            ret = await response.read()
    # nonebot.logger.info(ret)
    return ret
