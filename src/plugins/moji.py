from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random
import requests
import json
import time

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Referer': 'https://www.mojidict.com/',
    'origin': 'https://www.mojidict.com',
    # 'cookie': 'l=v',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 '
                  'Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400 '
}

# 冷却时间
moji_cd = 3
cd = {}

catch_str = on_keyword({'/moji '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    id = event.get_user_id()
    content = get_msg[6:]

    # 判断cd
    nowtime = time.time()
    if (nowtime - cd.get(event.user_id, 0)) < moji_cd:
        msg = "[CQ:at,qq={}]".format(id) + '你冲的太快啦，请休息一下吧'
        await catch_str.finish(Message(f'{msg}'))
        return
    else:
        cd[event.user_id] = nowtime

    json1 = await get_info(content)
    if json1 == "error":
        msg = "[CQ:at,qq={}]".format(id) + '接口返回错误，查询失败喵'
        await catch_str.finish(Message(f'{msg}'))
        return

    try:
        if len(json1['result']['searchResults']) > 0:
            msg = "[CQ:at,qq={}]".format(id) + "\n结果显示格式为：【 标题 】  解释\n"
            for i in range(len(json1['result']['searchResults'])):
                msg += " 【 " + json1['result']['searchResults'][i]['title'] + " 】  " + json1['result']['searchResults'][i]['excerpt'] + '\n'
            await catch_str.finish(Message(f'{msg}'))
        else:
            msg = "[CQ:at,qq={}]".format(id) + '查询无结果喵'
            await catch_str.finish(Message(f'{msg}'))
    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + '接口返回内容解析失败喵'
        await catch_str.finish(Message(f'{msg}'))


async def get_info(content):
    API_URL = 'https://api.mojidict.com/parse/functions/search_v3'
    # json传参不确定是否长期有效
    json1_str = '{"searchText":"' + content + '","langEnv":"zh-CN_ja","_SessionToken":"r:26c08f55e840395ab5d4e5e8fd5655af","_ClientVersion":"js3.4.1","_ApplicationId":"E62VyFVLMiW7kvbtVq3p","g_os":"PCWeb","_InstallationId":"22ca2d51-387c-4e96-8580-6cd1ada2b2fe"} '
    json1 = json.loads(json1_str)
    # nonebot.logger.info(json1)
    try:
        ret = requests.post(API_URL, json=json1, timeout=10, headers=headers)
        ret = ret.json()
    except requests.exceptions.RequestException as e:
        nonebot.logger.info(e)
        return "error"
    except IOError as e:
        nonebot.logger.info(e)
        return "error"
    # nonebot.logger.info(ret)

    return ret
