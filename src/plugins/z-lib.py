import aiohttp, json
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg


catch_str = on_command('z-lib', aliases={"搜书"})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    data = await get_data(content)

    if data == "error":
        msg = '命令错误，命令格式：/搜书 [书名]'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    data_json = json.loads(data)

    try:
        msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False) + '\n下载地址：https://gateway.pinata.cloud//ipfs/ 后面追加书的ipfs_cid即可。'
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

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
