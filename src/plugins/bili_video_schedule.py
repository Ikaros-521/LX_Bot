from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random
import requests

catch_str = on_keyword({'今日番剧'})


@catch_str.handle()
async def send_img(bot: Bot, event: Event, state: T_State):
    # get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    id = event.get_user_id()
    json1 = await get_info()
    if json1["code"] != 0:
        msg = "[CQ:at,qq={}]".format(id) + "\n接口获取数据异常，请联系管理员修复喵~"
        await catch_str.finish(Message(f'{msg}'))
        return
    try:
        out_str = "\n今日番剧如下：\n"
        for i in range(len(json1["result"][0]["episodes"])):
            out_str += "更新时间 " + json1["result"][0]["episodes"][i]["pub_time"] + " 【 " + \
                       json1["result"][0]["episodes"][i]["title"] + " 】 " + \
                       json1["result"][0]["episodes"][i]["pub_index"] + "\n"
        msg = "[CQ:at,qq={}]".format(id) + out_str
        await catch_str.finish(Message(f'{msg}'))
    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + "\n接口解析异常，请联系管理员修复喵~"
        await catch_str.finish(Message(f'{msg}'))


async def get_info():
    # 传参可以自行调整
    API_URL = 'https://api.bilibili.com/pgc/web/timeline?types=1&before=0&after=0'
    ret = requests.get(API_URL)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret
