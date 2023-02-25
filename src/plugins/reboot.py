from nonebot.adapters import Message
from nonebot import on_command
# from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import nonebot
# import socket
# import time
import os

# 重启功能
catch_str = on_command('reboot')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event):
    config = nonebot.get_driver().config

    # 只有超级管理员可以执行，配置云.env.prod文件中
    if id not in config.superusers:
        msg = "\n果咩，只有超级管理员可以执行"
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    # 执行linux系统命令进行重启，由于我这边由supervisord服务守护，所以是这样，请自行适配
    result = os.system('systemctl restart supervisord.service')
    nonebot.logger.info("result=" + str(result))
    msg = "\n重启返回=" + str(result)
    await catch_str.finish(Message(f'{msg}'), at_sender=True)
