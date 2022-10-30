from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random
import requests
import json
import time

headers1 = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'content-type': 'text/plain; charset=utf-8',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'content-type': 'application/json',
    'authorization': ''
}

# 冷却时间
cmd_cd = 1
# auth更新时间
auth_cd = 1800
cd = {}
# 上次运行时间
last_time = 0
first_run = 1

# 暂不可用
catch_str = on_keyword({'ms翻'})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    global first_run, last_time
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    id = event.get_user_id()
    content = get_msg[3:]

    # 判断cd
    nowtime = time.time()
    # nonebot.logger.info("nowtime=" + str(nowtime))
    if (nowtime - cd.get(event.user_id, 0)) < cmd_cd:
        msg = "[CQ:at,qq={}]".format(id) + '你冲的太快啦，请休息一下吧'
        await catch_str.finish(Message(f'{msg}'))
        return
    else:
        cd[event.user_id] = nowtime

    try:
        cmd = content[0:2]
        text = content[2:]
        # nonebot.logger.info("cmd=" + cmd + "|text=" + text)
        # 目前设计只支持中日互译
        if cmd == '中 ':
            src_lang = 'ja'
            tgt_lang = 'zh-CHS'
        elif cmd == '日 ':
            src_lang = 'zh-CHS'
            tgt_lang = 'ja'
        else:
            msg = "[CQ:at,qq={}]".format(id) + '\n命令类型错误，目前仅支持 日翻中和中翻日\n命令：【ms翻日 这样】'
            await catch_str.finish(Message(f'{msg}'))
            return
    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + '\n命令错误，目前仅支持 日翻中和中翻日\n命令：【ms翻日 这样】'
        await catch_str.finish(Message(f'{msg}'))
        return

    # 首次运行
    if first_run == 1:
        auth = await get_auth()
        if auth == "error":
            msg = "[CQ:at,qq={}]".format(id) + '\nauth接口返回错误，建议重新发送（再送を推奨）'
            await catch_str.finish(Message(f'{msg}'))
            return
        headers['authorization'] = "Bearer " + auth
        first_run = 0
    # 更新auth
    if (nowtime - last_time) >= auth_cd:
        auth = await get_auth()
        if auth == "error":
            msg = "[CQ:at,qq={}]".format(id) + '\nauth接口返回错误，建议重新发送（再送を推奨）'
            await catch_str.finish(Message(f'{msg}'))
            return
        headers['authorization'] = "Bearer " + auth

    last_time = nowtime
    # nonebot.logger.info(headers)
    json1 = await get_info(src_lang, tgt_lang, text)
    # nonebot.logger.info(json1)
    if json1 == "error":
        msg = "[CQ:at,qq={}]".format(id) + '\n接口返回错误，翻译失败（翻訳失敗）喵'
        await catch_str.finish(Message(f'{msg}'))
        return

    try:
        msg = "[CQ:at,qq={}]".format(id) + "\n" + json1[0]['translations'][0]['text']
        await catch_str.finish(Message(f'{msg}'))
    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + '\n接口返回错误，翻译失败（翻訳失敗）'
        await catch_str.finish(Message(f'{msg}'))


async def get_auth():
    API_URL = 'https://edge.microsoft.com/translate/auth'
    try:
        ret = requests.get(API_URL, timeout=10, headers=headers1)
        ret = ret.text
    except requests.exceptions.RequestException as e:
        nonebot.logger.info(e)
        return "error"
    except IOError as e:
        nonebot.logger.info(e)
        return "error"
    # nonebot.logger.info(ret)

    return ret


async def get_info(src_lang, tgt_lang, text):
    API_URL = 'https://api.cognitive.microsofttranslator.com/translate?from=' + src_lang + '&to=' + tgt_lang + \
              '&api-version=3.0&includeSentenceLength=true'
    payload = "[{\"Text\":\"" + text + "\"}]"
    # nonebot.logger.info(payload)
    bytedatas = payload.encode('UTF-8')  # 转换编码格式
    # nonebot.logger.info(bytedatas)
    try:
        ret = requests.post(API_URL, data=bytedatas, timeout=10, headers=headers)
        ret = ret.json()
    except requests.exceptions.RequestException as e:
        nonebot.logger.info(e)
        return "error"
    except IOError as e:
        nonebot.logger.info(e)
        return "error"
    # nonebot.logger.info(ret)

    return ret
