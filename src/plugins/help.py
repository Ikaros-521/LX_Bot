from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_keyword({'/help'})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    id = event.get_user_id()
    msg = "[CQ:at,qq={}]".format(id) + '\nLX_Bot在线帮助文档：https://docs.qq.com/sheet/DWURzcWhWR2tSTE10'

    await catch_str.finish(Message(f'{msg}'))
