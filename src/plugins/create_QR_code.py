from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_keyword({'/合成二维码 '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    id = event.get_user_id()
    get_msg = str(event.get_message())
    content = get_msg[7:]

    msg = "[CQ:image,file=https://api.linhun.vip/api/QRcode?url=" + content + "]"
    await catch_str.finish(Message(f'{msg}'))
