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

    json1 = await get_info(tag, r18)
    try:
        url = json1['data'][0]['urls']['original']
    except KeyError:
        id = event.get_user_id()
        msg = "[CQ:at,qq={}]".format(id) + '搜图出错'
        await catch_str.finish(Message(f'{msg}'))
        return

    msg = "[CQ:image,file=" + url + "]"
    await catch_str.finish(Message(f'{msg}'))


async def get_info(tag, r18):
    API_URL = 'https://api.lolicon.app/setu/v2?tag=' + tag + '&r18=' + r18 + '&?' + str(random.random())
    ret = requests.get(API_URL)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret
