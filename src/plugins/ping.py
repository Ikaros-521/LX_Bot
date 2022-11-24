import aiohttp
from nonebot.adapters import Message
from nonebot import on_keyword
from nonebot.typing import T_State
# from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import nonebot
import random
import requests

catch_str = on_keyword({'/ping '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[6:]
    ret = await start(content)
    id = event.get_user_id()
    msg = "[CQ:at,qq={}]".format(id) + "\n" + ret
    await catch_str.finish(Message(f'{msg}'))


async def start(content):
    API_URL = 'https://shengapi.cn/api/ping.php?host=' + content
    header1 = {
        'content-type': 'text/plain; charset=utf-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
    }
    async with aiohttp.ClientSession(headers=header1) as session:
        async with session.get(url=API_URL, headers=header1) as response:
            ret = await response.read()
    # nonebot.logger.info(ret)
    return ret.decode('utf-8')
