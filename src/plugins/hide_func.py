from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_keyword({'/隐藏功能'})

@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    id = event.get_user_id()
    msg = "[CQ:at,qq={}]".format(id) + '\n目前支持命令为：\n/cos 随机返回一张cos图片\n/查火羽 懂的都懂'
    await catch_str.finish(Message(f'{msg}'))
