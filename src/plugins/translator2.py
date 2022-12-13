# import nonebot
import json

import aiohttp
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.typing import T_State
from aiocqhttp.exceptions import Error as CQHttpError
from nonebot.rule import Rule


tran = on_command('翻译2', priority=1)


@tran.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["translate"] = args


@tran.got("res", prompt="请问你要翻译的句子是？")
async def handle_city(bot: Bot, event: Event, state: T_State):
    translate = state["res"]
    API_URL = f'http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i={translate}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.warning(resp)
    result = ret['translateResult'][0][0]['tgt']
    result = '\n翻译结果：' + result

    try:
        await tran.finish(Message(f'{result}'), at_sender=True)
    except CQHttpError:
        pass