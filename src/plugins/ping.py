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
    msg = "[CQ:at,qq={}]".format(id) + ret
    await catch_str.finish(Message(f'{msg}'))


async def start(content):
    API_URL = 'https://shengapi.cn/api/ping.php?host=' + content
    ret = requests.get(API_URL)
    ret = ret.text
    # nonebot.logger.info(ret)
    return ret
