import aiohttp
from nonebot.adapters import Message
from nonebot import on_command
from nonebot.params import CommandArg
# from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
# import nonebot
# import random

catch_str = on_command('ping')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    ret = await start(content)
    msg = "\n" + ret
    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def start(content):
    API_URL = 'https://api.juncikeji.xyz/api/ping.php?ip=' + content
    header1 = {
        'content-type': 'text/plain; charset=utf-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
    }
    async with aiohttp.ClientSession(headers=header1) as session:
        async with session.get(url=API_URL, headers=header1) as response:
            ret = await response.read()
    # nonebot.logger.info(ret)
    return ret.decode('utf-8')
