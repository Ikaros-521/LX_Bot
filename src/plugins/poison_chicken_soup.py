import json

import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import requests

catch_str = on_keyword({'/毒鸡汤'})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    id = event.get_user_id()

    data = await get_data()
    msg = '\n' + data['msg']

    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data():
    API_URL = 'https://api.linhun.vip/api/dujitang'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret
