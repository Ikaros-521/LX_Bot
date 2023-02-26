import aiohttp
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
# import nonebot
# import random

catch_str = on_command('端口扫描')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    ret = await start(content)
    msg = "\n" + ret
    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def start(content):
    ipport = content.split(' ')
    apiKey = '427337dfa9dd77b66065ce1bd7af076e'
    API_URL = 'https://shengapi.cn/api/openport.php?' + ipport[0] + '&' + ipport[1] + '&apiKey=' + apiKey
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            ret = await response.read()
    # nonebot.logger.info(ret)
    return ret.decode('utf-8')
