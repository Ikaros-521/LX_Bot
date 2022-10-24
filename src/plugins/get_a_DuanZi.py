from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import requests

catch_str = on_keyword({'/来个段子'})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    id = event.get_user_id()

    data = await get_data()
    msg = "[CQ:at,qq={}]".format(id) + '\n' + data['mum']

    await catch_str.finish(Message(f'{msg}'))


async def get_data():
    API_URL = 'https://api.linhun.vip/api/duanzi'
    ret = requests.get(API_URL)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret
