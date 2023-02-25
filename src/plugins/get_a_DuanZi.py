import json

import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
# from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_command('来个段子')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event):
    data = await get_data()
    try:
        msg = '\n' + data['mum']
    except:
        msg = '接口又寄了，宝~'

    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data():
    apiKey = '4cbbf53cfd186aa072a1092b94ef0bd6'
    API_URL = 'https://api.linhun.vip/api/duanzi' + '?apiKey=' + apiKey
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret
