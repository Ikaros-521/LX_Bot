import aiohttp
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import nonebot
# import random

catch_str = on_keyword({'/端口扫描 '})


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
    ipport = content.split(' ')
    apiKey = '427337dfa9dd77b66065ce1bd7af076e'
    API_URL = 'https://shengapi.cn/api/openport.php?' + ipport[0] + '&' + ipport[1] + '&apiKey=' + apiKey
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            ret = await response.read()
    # nonebot.logger.info(ret)
    return ret.decode('utf-8')
