import json

import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_command('彩虹屁')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    data = await get_data()
    msg = '\n' + data['data']['text']

    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data():
    API_URL = 'https://api.shadiao.pro/chp'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret