from nonebot.adapters.onebot.v11 import Message
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_command('help')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event):
    id = event.get_user_id()
    msg = '\nLX_Bot在线帮助文档：https://docs.qq.com/sheet/DWURzcWhWR2tSTE10'

    await catch_str.finish(Message(f'{msg}'), at_sender=True)
