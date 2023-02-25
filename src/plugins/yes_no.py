from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event
# import nonebot
import random

catch_str = on_command('是否')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    random_num = random.randint(1, 3)
    ret_str = ''
    if random_num == 1:
        ret_str = '是'
    elif random_num == 2:
        ret_str = '你确定想知道结果？？？'
    else:
        ret_str = '否'
    msg = '\n判断内容：' + content + '\n判断结果：' + ret_str
    await catch_str.finish(Message(f'{msg}'), at_sender=True)

