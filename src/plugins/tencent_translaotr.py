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
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

# 冷却时间
moji_cd = 1
cd = {}

# 暂不可用
catch_str = on_keyword({'tx翻'})


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
        cmd = content[0:2]
        text = content[2:]
        # nonebot.logger.info("cmd=" + cmd + "|text=" + text)
        # 目前设计只支持中日互译
        if cmd == '中 ':
            src_lang = 'jp'
            tgt_lang = 'zh'
        elif cmd == '日 ':
            src_lang = 'zh'
            tgt_lang = 'jp'
        else:
            msg = "[CQ:at,qq={}]".format(id) + '\n命令类型错误，目前仅支持 日翻中和中翻日\n命令：【tx翻日 这样】'
            await catch_str.finish(Message(f'{msg}'))
            return
    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + '\n命令错误，目前仅支持 日翻中和中翻日\n命令：【tx翻日 这样】'
        await catch_str.finish(Message(f'{msg}'))
        return

    json1 = await get_info(src_lang, tgt_lang, text)
    nonebot.logger.info(json1)
    if json1 == "error":
        msg = "[CQ:at,qq={}]".format(id) + '\n接口返回错误，翻译失败（翻訳失敗）喵'
        await catch_str.finish(Message(f'{msg}'))
        return

    try:
        msg = "[CQ:at,qq={}]".format(id) + "\n" + json1['translate']['records'][0]['targetText']
        await catch_str.finish(Message(f'{msg}'))
    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + '\n接口返回错误，翻译失败（翻訳失敗）'
        await catch_str.finish(Message(f'{msg}'))


async def get_info(src_lang, tgt_lang, text):
    API_URL = 'https://fanyi.qq.com/api/translate'
    payload = "source=" + src_lang + "&target=" + tgt_lang + "&sourceText=" + text + "&qtv=55cbf2fd1148af1e&qtk=AFOBVuJJRn0fdf1BspBZc1QYJEk0pVZbnGMuRQnsT%2BGFbcmepBgfkB1O9Ofxc39sGYAtYVN1pGIWgSFAU0C6ZdI8k%2FSO93nZhcCL7kDsptPSPNgLy7H2DKoCN8y%2BgbZgBt14rqJO4qAoQ%2BiSsHq5ZA%3D%3D&ticket=&randstr=&sessionUuid=translate_uuid1667118326920 "
    # payload = "source=zh&target=jp&sourceText=在吗&qtv=55cbf2fd1148af1e&qtk=AFOBVuJJRn0fdf1BspBZc1QYJEk0pVZbnGMuRQnsT%2BGFbcmepBgfkB1O9Ofxc39sGYAtYVN1pGIWgSFAU0C6ZdI8k%2FSO93nZhcCL7kDsptPSPNgLy7H2DKoCN8y%2BgbZgBt14rqJO4qAoQ%2BiSsHq5ZA%3D%3D&ticket=&randstr=&sessionUuid=translate_uuid1667118326920"
    nonebot.logger.info(payload)
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
