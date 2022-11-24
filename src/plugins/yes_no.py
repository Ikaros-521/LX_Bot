from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random

catch_str = on_keyword({'/是否 '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[4:]
    random_num = random.randint(1, 3)
    ret_str = ''
    if random_num == 1:
        ret_str = '是'
    elif random_num == 2:
        ret_str = '你确定想知道结果？？？'
    else:
        ret_str = '否'
    id = event.get_user_id()
    msg = '\n判断内容：' + content + '\n判断结果：' + ret_str
    await catch_str.finish(Message(f'{msg}'), at_sender=True)
