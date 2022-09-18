from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random

catch_str = on_keyword({'/cos2'})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    # get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    # id = event.get_user_id()
    msg = "[CQ:image,file=https://api.linhun.vip/api/Littlesister?" + str(random.random()) + "]"

    await catch_str.finish(Message(f'{msg}'))
    # await catch_str.finish(Message(MessageSegment.image('https://api.vvhan.com/api/girl?2')))
