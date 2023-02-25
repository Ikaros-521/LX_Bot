import json
import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
# import nonebot
# import random

catch_str = on_command('今日番剧')

@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    json1 = await get_info(1, 0, 0)
    if json1["code"] != 0:
        msg = "\n接口获取数据异常，请联系管理员修复喵~"
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    try:
        out_str = "\n今日番剧如下：\n"
        for i in range(len(json1["result"][0]["episodes"])):
            out_str += "更新时间 " + json1["result"][0]["episodes"][i]["pub_time"] + " 【 " + \
                       json1["result"][0]["episodes"][i]["title"] + " 】 " + \
                       json1["result"][0]["episodes"][i]["pub_index"] + "\n"
        await catch_str.finish(Message(f'{out_str}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        msg = "\n接口解析异常，请联系管理员修复喵~"
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


catch_str2 = on_command('昨日番剧')

@catch_str2.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    json1 = await get_info(1, 1, 0)
    if json1["code"] != 0:
        msg = "\n接口获取数据异常，请联系管理员修复喵~"
        await catch_str2.finish(Message(f'{msg}'), at_sender=True)
    try:
        out_str = "\n昨日番剧如下：\n"
        for i in range(len(json1["result"][0]["episodes"])):
            out_str += "更新时间 " + json1["result"][0]["episodes"][i]["pub_time"] + " 【 " + \
                       json1["result"][0]["episodes"][i]["title"] + " 】 " + \
                       json1["result"][0]["episodes"][i]["pub_index"] + "\n"
        await catch_str2.finish(Message(f'{out_str}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        msg = "\n接口解析异常，请联系管理员修复喵~"
        await catch_str2.finish(Message(f'{msg}'), at_sender=True)


catch_str3 = on_command('明日番剧')

@catch_str3.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    json1 = await get_info(1, 0, 1)
    if json1["code"] != 0:
        msg = "\n接口获取数据异常，请联系管理员修复喵~"
        await catch_str3.finish(Message(f'{msg}'), at_sender=True)
    try:
        out_str = "\n明日番剧如下：\n"
        for i in range(len(json1["result"][1]["episodes"])):
            out_str += "更新时间 " + json1["result"][1]["episodes"][i]["pub_time"] + " 【 " + \
                       json1["result"][1]["episodes"][i]["title"] + " 】 " + \
                       json1["result"][1]["episodes"][i]["pub_index"] + "\n"
        await catch_str3.finish(Message(f'{out_str}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        msg = "\n接口解析异常，请联系管理员修复喵~"
        await catch_str3.finish(Message(f'{msg}'), at_sender=True)


async def get_info(type=1, before=0, after=0):
    # 传参可以自行调整
    API_URL = 'https://api.bilibili.com/pgc/web/timeline?types=' + str(type) + '&before=' + str(before) + '&after=' + str(after)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                result = await response.read()
                ret = json.loads(result)
        # nonebot.logger.info(ret)
        return ret
    except:
        return None
