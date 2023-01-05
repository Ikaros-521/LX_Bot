import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
# import random
import json
import time

header1 = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'content-type': 'text/plain; charset=utf-8',
}

header = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'content-type': 'application/json',
    'authorization': ''
}

# 冷却时间（秒）
cmd_cd = 1
# auth更新时间（秒）
auth_cd = 1800
cd = {}
# 上次运行时间
last_time = 0

catch_str = on_keyword({'ms翻'})


@catch_str.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global first_run, last_time
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[3:]

    # 判断cd
    nowtime = time.time()
    # nonebot.logger.info("nowtime=" + str(nowtime))
    if (nowtime - cd.get(event.user_id, 0)) < cmd_cd:
        msg = '你冲的太快啦，请休息一下吧'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    else:
        cd[event.user_id] = nowtime

    try:
        cmd = content[0:2]
        text = content[2:]
        # nonebot.logger.info("cmd=" + cmd + "|text=" + text)
        # 目前设计 翻日、翻中、翻英、翻韩
        if cmd == '中 ':
            src_lang = 'ja'
            tgt_lang = 'zh-CHS'
        elif cmd == '日 ':
            src_lang = 'zh-CHS'
            tgt_lang = 'ja'
        elif cmd == '英 ':
            src_lang = 'zh-CHS'
            tgt_lang = 'en'
        elif cmd == '韩 ':
            src_lang = 'zh-CHS'
            tgt_lang = 'ko'
        else:
            msg = '\n命令类型错误，目前支持 翻日、翻中、翻英、翻韩\n命令：【ms翻日 这样】'
            await catch_str.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        msg = '\n命令错误，目前仅支持 翻日、翻中、翻英、翻韩\n命令：【ms翻日 这样】'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    # 更新auth，一次重试
    if (nowtime - last_time) >= auth_cd:
        auth = await get_auth()
        if auth == "error":
            auth = await get_auth()
            if auth == "error":
                msg = '\nauth接口返回错误，建议重新发送（再送を推奨）'
                await catch_str.finish(Message(f'{msg}'), at_sender=True)
        # 设置请求头中的鉴权
        header['authorization'] = "Bearer " + auth

    last_time = nowtime
    # nonebot.logger.info(headers)
    json1 = await get_info(src_lang, tgt_lang, text)
    # nonebot.logger.info(json1)
    if json1 == "error":
        msg = '\n接口返回错误，翻译失败（翻訳失敗）喵'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    try:
        msg = "\n" + json1[0]['translations'][0]['text']
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        msg = '\njson内容错误，翻译失败（翻訳失敗）'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


# 获取鉴权
async def get_auth():
    API_URL = 'https://edge.microsoft.com/translate/auth'
    try:
        async with aiohttp.ClientSession(headers=header1) as session:
            async with session.get(url=API_URL, timeout=10, headers=header1) as response:
                ret = await response.read()
        # nonebot.logger.info(ret)
    except:
        return "error"
    return ret.decode('utf-8')


# 获取翻译结果
async def get_info(src_lang, tgt_lang, text):
    src_lang = ""
    API_URL = 'https://api.cognitive.microsofttranslator.com/translate?from=' + src_lang + '&to=' + tgt_lang + \
              '&api-version=3.0&includeSentenceLength=true'
    payload = "[{\"Text\":\"" + text + "\"}]"
    # nonebot.logger.info(payload)
    bytedatas = payload.encode('UTF-8')  # 转换编码格式
    # nonebot.logger.info(bytedatas)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=API_URL, data=bytedatas, timeout=10, headers=header) as response:
                result = await response.read()
                ret = json.loads(result)
    except:
        return "error"
    # nonebot.logger.info(ret)

    return ret
