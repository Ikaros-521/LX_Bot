import json

import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_command("圣经", aliases={"互联网圣经"})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    data = await get_data()
    try:
        msg = '\n' + data['text']
    except:
        msg = "\n接口返回数据异常，请联系管理员修复。"

    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data():
    header1 = {
        'content-type': 'text/plain; charset=utf-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
    }
    API_URL = 'https://api.azite.cn/bible?type=json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL, headers=header1) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret
