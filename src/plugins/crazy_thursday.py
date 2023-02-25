import json

import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
# from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_command('疯狂星期四')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event):
    data = await get_data()
    try:
        msg = '\n' + data['data']['text']
    except:
        msg = "请求返回错误，可能是网络问题或者API寄了"

    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data():
    API_URL = 'https://api.shadiao.pro/kfc'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret
