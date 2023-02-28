from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random

catch_str = on_command('求签')


@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    random_num = random.randint(1, 7)
    ret_str = ''
    if random_num == 1:
        ret_str = '大吉'
    elif random_num == 2:
        ret_str = '中吉'
    elif random_num == 3:
        ret_str = '小吉'
    elif random_num == 4:
        ret_str = '吉'
    elif random_num == 5:
        ret_str = '末吉'
    else:
        ret_str = '凶'
    id = event.get_user_id()
    msg = '\n求签内容：' + content + '\n求签结果：' + ret_str
    await catch_str.finish(Message(f'{msg}'), at_sender=True)
