# import datetime
import json

import aiohttp
import nonebot
# import requests
# import time
# from io import BytesIO
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.typing import T_State
from nonebot_plugin_imageutils import Text2Image

catch_str = on_keyword({'/base64 '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    id = event.get_user_id()
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[8:]

    # 以空格分割 类型（加密/解密） 加解密的内容
    content = content.split()
    type = ""
    msg = ""

    if len(content) > 1:
        type = content[0]
        msg = content[1]
    else:
        msg = "[CQ:at,qq={}]".format(id) + '传参错误，命令格式【/base64 加密/解密 加解密内容】'
        await catch_str.finish(Message(f'{msg}'))
        return

    if type == '加密':
        type = 'jiami'
    elif type == '解密':
        type = 'jiemi'
    else:
        msg = "[CQ:at,qq={}]".format(id) + '传参错误，命令格式【/base64 加密/解密 加解密内容】'
        await catch_str.finish(Message(f'{msg}'))
        return

    data = await get_info(type, msg)

    try:
        # 判断返回代码
        if data['code'] != 200:
            msg = "[CQ:at,qq={}]".format(id) + '接口返回失败'
            await catch_str.finish(Message(f'{msg}'))
            return
        else:
            if type == 'jiami':
                msg = "[CQ:at,qq={}]".format(id) + '\n加密为：' + data['encryption']
            else:
                msg = "[CQ:at,qq={}]".format(id) + '\n解密为：' + data['decrypt']
            await catch_str.finish(Message(f'{msg}'))
            return
    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + '解析失败，请检查解析内容'
        await catch_str.finish(Message(f'{msg}'))
        return


async def get_info(type, msg):
    API_URL = 'https://api.linhun.vip/api/base64?type=' + type + '&text=' + msg
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret
