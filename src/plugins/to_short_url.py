from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import nonebot
import requests

catch_str = on_keyword({'/短链 '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    src = get_msg[4:]
    url = await get_short_url(src)

    id = event.get_user_id()
    msg = "[CQ:at,qq={}]".format(id) + '\n短链为：' + url
    await catch_str.finish(Message(f'{msg}'))


async def get_short_url(src):
    API_URL = 'https://shengapi.cn/api/dwz.php?url=' + src
    ret = requests.get(API_URL)
    ret = ret.text
    # nonebot.logger.info(ret)
    return ret
