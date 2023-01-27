from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg
import re
import json
import aiohttp
import nonebot

catch_str = on_command('tt2')

@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    ret = await get_data(content)
    try:
        await catch_str.send(MessageSegment.record(file=ret))
    except:
        msg = '发送音频失败，请检查接口是否正常'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data(content):
    # 更换为直接返回音频文件的API，也可以直接使用
    API_URL = 'http://127.0.0.1:56789/tt2/content=' + content
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            ret = await response.read()
    return ret
