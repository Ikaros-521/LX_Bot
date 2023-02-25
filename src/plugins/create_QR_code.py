from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_command('合成二维码')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    msg = "[CQ:image,file=https://api.linhun.vip/api/QRcode?url=" + content + "]"
    await catch_str.finish(Message(f'{msg}'))
