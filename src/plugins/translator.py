import json

import aiohttp
import nonebot
from nonebot import on_command
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.typing import T_State
from aiocqhttp.exceptions import Error as CQHttpError
from nonebot.rule import Rule

catch_str = on_keyword({'/翻译 '})


@catch_str.handle()
async def get_short_url(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    translate = get_msg[4:]
    nonebot.logger.info(translate)
    API_URL = f'http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i={translate}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.warning(resp)
    result = ret['translateResult'][0][0]['tgt']
    result = '\n翻译结果：' + result

    try:
        await catch_str.finish(Message(f'{result}'), at_sender=True)
    except CQHttpError:
        pass
