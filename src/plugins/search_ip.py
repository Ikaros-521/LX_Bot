from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import requests

catch_str = on_keyword({'/查ip '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    id = event.get_user_id()
    get_msg = str(event.get_message())
    content = get_msg[5:]

    data = await get_data(content)
    msg = "[CQ:at,qq={}]".format(id) + '\n' + data

    await catch_str.finish(Message(f'{msg}'))


async def get_data(content):
    API_URL = 'https://api.linhun.vip/api/iplocation?ip=' + content
    ret = requests.get(API_URL)
    ret = ret.text
    # nonebot.logger.info(ret)
    return ret
