# import nonebot
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.typing import T_State
from aiocqhttp.exceptions import Error as CQHttpError
from nonebot.rule import Rule
import requests


tran = on_command('翻译2', priority=1)


@tran.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["translate"] = args


@tran.got("res", prompt="请问你要翻译的句子是？")
async def handle_city(bot: Bot, event: Event, state: T_State):
    translate = state["res"]
    url = f'http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i={translate}'
    resp = requests.get(url).json()
    # nonebot.logger.warning(resp)
    result = resp['translateResult'][0][0]['tgt']
    id = event.get_user_id()
    result = "[CQ:at,qq={}]".format(id) + '\n翻译结果：' + result

    try:
        await tran.finish(Message(f'{result}'))
    except CQHttpError:
        pass