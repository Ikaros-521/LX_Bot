from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg
import re
import json
import aiohttp
import nonebot

# 暂不可用
catch_str = on_command('tts')

@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    content = content.split()

    data_json = {
        "text":"",
        "speaker":"",
        "source":"原神",
        "speed":1,
        "model":"genshin",
        "language":"ZH",
        "cleaned":False,
        "noisew":0.8,
        "noise":0.667
    }

    if len(content) == 1:
        msg = '传参错误，命令格式【/语音[角色名] [待转换文本] [语速(数字，例如：1.0)] [感情等变化程度(数字，例如：0.8)] [音素发音长度变化程度(数字，例如：0.667)]】'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    elif len(content) > 4:
        data_json["speaker"] = content[0]
        data_json["text"] = content[1]

        if is_number(content[2]) and is_number(content[3]) and is_number(content[4]):
            data_json["speed"] = float(content[2])
            data_json["noise"] = float(content[3])
            data_json["noisew"] = float(content[4])
        else:
            msg = '传参错误，命令格式【/语音[角色名] [待转换文本] [语速(数字，例如：1.0)] [感情等变化程度(数字，例如：0.8)] [音素发音长度变化程度(数字，例如：0.667)]】'
            await catch_str.finish(Message(f'{msg}'), at_sender=True)
    elif len(content) > 3:
        data_json["speaker"] = content[0]
        data_json["text"] = content[1]

        if is_number(content[2]) and is_number(content[3]):
            data_json["speed"] = float(content[2])
            data_json["noise"] = float(content[3])
        else:
            msg = '传参错误，命令格式【/语音[角色名] [待转换文本] [语速(数字，例如：1.0)] [感情等变化程度(数字，例如：0.8)] [音素发音长度变化程度(数字，例如：0.667)]】'
            await catch_str.finish(Message(f'{msg}'), at_sender=True)
    elif len(content) > 2:
        data_json["speaker"] = content[0]
        data_json["text"] = content[1]

        if is_number(content[2]):
            data_json["speed"] = float(content[2])
        else:
            msg = '传参错误，命令格式【/语音[角色名] [待转换文本] [语速(数字，例如：1.0)] [感情等变化程度(数字，例如：0.8)] [音素发音长度变化程度(数字，例如：0.667)]】'
            await catch_str.finish(Message(f'{msg}'), at_sender=True)
    elif len(content) > 1:
        data_json["speaker"] = content[0]
        data_json["text"] = content[1]
    else:
        msg = '传参错误，命令格式【/语音[角色名] [待转换文本] [语速(数字，例如：1.0)] [感情等变化程度(数字，例如：0.8)] [音素发音长度变化程度(数字，例如：0.667)]】'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    json1 = await get_data(data_json)
    try:
        await catch_str.send(MessageSegment.record(file=json1["data"]))
    except:
        msg = '发送音频失败，请检查接口是否正常'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data(data_json):
    header1 = {
        'accept': 'application/json, text/plain, */*',
        #'mt_version': '1673105130033',
        'origin': 'https://tools.miku.ac',
        'referer': 'https://tools.miku.ac/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/88.0.4324.192 Safari/537.36',
        'authsign': '829f9477931963815d243288ee57b27bbd7ffd1fd74d62477a9174cc5f4017f9.U2FsdGVkX19tdrhiVXLZeqY2aGLZlg8+e06/u/jQ5cA=',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': 'connect.sid=s%3Aac5f2b57-fc55-4dc4-b5c9-dacb0d38c4f8.RlTqqTzV%2Bw0V9x%2BRuAYycgL2DBDRCENfl7NQjRRpo8I'
    }
    API_URL = 'https://api.okmiku.com/anime_tts'
    async with aiohttp.ClientSession() as session:
        async with session.post(url=API_URL, headers=header1, json=data_json) as response:
            result = await response.read()
            ret = json.loads(result)
    nonebot.logger.info(ret)
    return ret


# 是否是数字
def is_number(num):
    pattern = re.compile(r'(.*)\.(.*)\.(.*)')
    if pattern.match(num):
        return False
    return num.replace(".", "").isdigit()