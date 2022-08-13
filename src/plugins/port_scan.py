from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import nonebot
import random
import requests

catch_str = on_keyword({'/端口扫描 '})


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
    ipport = content.split(' ')
    API_URL = 'https://shengapi.cn/api/openport.php?' + ipport[0] + '&' + ipport[1]
    ret = requests.get(API_URL)
    ret = ret.text
    # nonebot.logger.info(ret)
    return ret
