import requests
import random
import json

from nonebot import on_command, on_keyword
from nonebot.adapters import Bot, Message, Event
from nonebot.typing import T_State
from nonebot.rule import Rule
import nonebot


async def translator(q):
    token = '【调用鉴权接口获取的token】'
    url = 'https://aip.baidubce.com/rpc/2.0/mt/texttrans-with-dict/v1?access_token=' + token

    # q = '输入query'  # example: hello

    # For list of language codes, please refer to `https://ai.baidu.com/ai-doc/MT/4kqryjku9#语种列表`
    from_lang = 'jp'  # example: en
    to_lang = 'zh'  # example: zh
    term_ids = ''  # 术语库ID，多个逗号隔开

    # Build request
    headers = {'Content-Type': 'application/json'}
    payload = {'q': q, 'from': from_lang, 'to': to_lang, 'termIds': term_ids}

    nonebot.logger.info(url)
    nonebot.logger.info(payload)

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    nonebot.logger.info(result)

    # Show response
    return result


# async def _checker(bot: Bot, event: Event, state: T_State) -> bool:
#     return isinstance(event, MessageEvent)


# tran = on_command('日语', aliases={""}, priority=1, rule=Rule(_checker))


# @tran.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["translate"] = args


#@tran.got("res", prompt="请问你要翻译的句子是？")
async def handle_city(bot: Bot, event: Event, state: T_State):
    translate = state["res"]
    result = await translator(translate)
    id = event.get_user_id()
    result = "[CQ:at,qq={}]".format(id) + '翻译结果：' + result
    result = Message(result)

    # try:
    #     await tran.send(result)
    # except CQHttpError:
    #     pass
