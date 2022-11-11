from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random

from .data import DATA

catch_str = on_keyword({'/发病 '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    id = event.get_user_id()
    # nonebot.logger.info(get_msg)
    content = get_msg[4:]

    random_num = random.randint(1, len(DATA)) - 1

    msg = "[CQ:at,qq={}]".format(id) + '\n'
    msg += DATA[random_num].format(target_name=content)

    await catch_str.finish(Message(f'{msg}'))
