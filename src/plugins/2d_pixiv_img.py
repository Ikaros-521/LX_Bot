import json

import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random
import requests

catch_str = on_keyword({'/r18 '})


@catch_str.handle()
async def send_img(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[5:]

    tag = ""
    r18 = "0"
    # 以空格分割 标签 r18开关
    content = content.split()

    if len(content) > 0:
        tag = content[0]
    if len(content) > 1:
        if content[1] == "1":
            r18 = "1"

    id = event.get_user_id()
    json1 = await get_info(tag, r18)
    try:
        url = json1['data'][0]['urls']['original']
    except KeyError:
        msg = "[CQ:at,qq={}]".format(id) + '搜图出错'
        await catch_str.finish(Message(f'{msg}'))
        return

    # url = await get_short_url(url)
    # msg = "[CQ:at,qq={}]".format(id) + url
    # await catch_str.finish(Message(f'{msg}'))
    msg = "[CQ:image,file=" + url + ",type=flash]"
    await catch_str.finish(Message(f'{msg}'))


async def get_info(tag, r18):
    API_URL = 'https://api.lolicon.app/setu/v2?tag=' + tag + '&r18=' + r18 + '&?' + str(random.random())
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret


async def get_short_url(src):
    API_URL = 'https://shengapi.cn/api/dwz.php?url=' + src
    ret = requests.get(API_URL)
    ret = ret.text
    # nonebot.logger.info(ret)
    return ret