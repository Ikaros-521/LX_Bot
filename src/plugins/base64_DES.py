# import datetime
import json
import aiohttp
# import nonebot
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message


catch_str = on_command('base64')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    # 以空格分割 类型（加密/解密） 加解密的内容
    content = content.split()
    type = ""
    msg = ""

    if len(content) > 1:
        type = content[0]
        msg = content[1]
    else:
        msg = '传参错误，命令格式【/base64 加密/解密 加解密内容】'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    if type == '加密':
        type = 'jiami'
    elif type == '解密':
        type = 'jiemi'
    else:
        msg = '传参错误，命令格式【/base64 加密/解密 加解密内容】'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    data = await get_info(type, msg)

    try:
        # 判断返回代码
        if data['code'] != 200:
            msg = '接口返回失败'
            await catch_str.finish(Message(f'{msg}'), at_sender=True)
        else:
            if type == 'jiami':
                msg = '\n加密为：' + data['encryption']
            else:
                msg = '\n解密为：' + data['decrypt']
            await catch_str.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        msg = '解析失败，请检查解析内容'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_info(type, msg):
    # 替换自己的api key
    apiKey = '4eb0e808bff486e10b930bbfe955e145'
    API_URL = 'https://api.linhun.vip/api/base64?type=' + type + '&text=' + msg + '&apiKey=' + apiKey
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret
