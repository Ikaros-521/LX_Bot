from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import random

catch_str = on_keyword({'发表情'})

@catch_str.handle()
async def send_msg(bot: Bot, event: Event):

    emoji_msg = "[CQ:face,id=" + str(random.randint(0, 221)) + "]"
    await catch_str.send(Message(emoji_msg))
