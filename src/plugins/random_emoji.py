from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message

catch_str = on_keyword({'发表情'})

@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):

    emoji_msg = "[CQ:face,id=12]"
    await catch_str.send(Message(emoji_msg))
