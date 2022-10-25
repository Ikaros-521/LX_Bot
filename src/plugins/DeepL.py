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
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Referer': 'https://www.deepl.com/',
    'origin': 'https://www.deepl.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 '
                  'Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400 ',
    # cookie自行替换
    'cookie': ''
}

# 冷却时间
moji_cd = 1
cd = {}


# deepL功能暂不可用
catch_str = on_keyword({'dl '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    id = event.get_user_id()
    content = get_msg[3:]

    # 判断cd
    nowtime = time.time()
    # nonebot.logger.info("nowtime=" + str(nowtime))
    if (nowtime - cd.get(event.user_id, 0)) < moji_cd:
        msg = "[CQ:at,qq={}]".format(id) + '你冲的太快啦，请休息一下吧'
        await catch_str.finish(Message(f'{msg}'))
        return
    else:
        cd[event.user_id] = nowtime

    try:
        cmd = content[0:4]
        text = content[4:]
        # nonebot.logger.info("cmd=" + cmd + "|text=" + text)
        if cmd == '日翻中 ':
            src_lang = 'JA'
            tgt_lang = 'ZH'
        elif cmd == '中翻日 ':
            src_lang = 'ZH'
            tgt_lang = 'JA'
        else:
            msg = "[CQ:at,qq={}]".format(id) + '\n命令类型错误，目前仅支持 日翻中和中翻日\n命令：【dl 中翻日 这样】'
            await catch_str.finish(Message(f'{msg}'))
            return
    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + '\n命令错误，目前仅支持 日翻中和中翻日\n命令：【dl 中翻日 这样】'
        await catch_str.finish(Message(f'{msg}'))
        return

    json1 = await get_info(src_lang, tgt_lang, text)
    if json1 == "error":
        msg = "[CQ:at,qq={}]".format(id) + '\n接口返回错误，翻译失败（翻訳失敗）喵'
        await catch_str.finish(Message(f'{msg}'))
        return

    try:
        if len(json1['result']['translations'][0]['beams']) > 0:
            msg = "[CQ:at,qq={}]".format(id) + "\n" + json1['result']['translations'][0]['beams'][0]['sentences'][0]['text']
            await catch_str.finish(Message(f'{msg}'))
        else:
            msg = "[CQ:at,qq={}]".format(id) + '\n翻译无结果喵（翻訳結果なし）'
            await catch_str.finish(Message(f'{msg}'))
    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + '\n接口返回错误，翻译失败（翻訳失敗）'
        await catch_str.finish(Message(f'{msg}'))


async def get_info(src_lang, tgt_lang, text):
    nowtime = int(time.time() * 1000)
    # nonebot.logger.info("nowtime=" + str(nowtime))
    API_URL = 'https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs'
    # json传参不确定是否长期有效
    json1_str = '{"jsonrpc":"2.0","method" : "LMT_handle_jobs","params":{"jobs":[{"kind":"default","sentences":[{' \
                '"text":"' + text + '","id":0,"prefix":""}],"raw_en_context_before":[],"raw_en_context_after":[],' \
                '"preferred_num_beams":4}],"lang":{"preference":{"weight":{},"default":"default"},' \
                '"source_lang_computed":"' + src_lang + '","target_lang":"' + tgt_lang + '"},"priority":1,' \
                '"commonJobParams":{"mode":"translate","browserType":1,"formality":null},"timestamp":' + \
                str(nowtime) + '},"id":68910007} '
    json1 = json.loads(json1_str)
    nonebot.logger.info(json1)
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
