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
    'Content-Type': 'application/json',
    # 'Referer': 'https://fanyi.sogou.com',
    'Origin': 'https://fanyi.sogou.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 '
                  'Safari/537.36 Core/1.94.178.400 QQBrowser/11.2.5170.400',
    'sec-ch-ua-mobile': 'same-origin',
    'Sec-Fetch-Site': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Q-INFO': 'WyKcqXKyGTRJ8cVla5D0INDleUGCeQMmowmelk72pOOtDpZ2A04ho/NyUvtVzk/i944bYSxG21yTuaYWNTuQdbO2yaF'
              '+00vVOnuH1wXIcbdgqtl9reFByf6FxezeiU1ygoBXylH9cRtsxabFU0YX+6vsbwywob4n18YRBwO3AMw48KoZWpUWVltfPk1spJlC'
              '/3BayACQmRL3sKISyB1UHYrhC/1ZyHIwE3ydYbdk9F9KEWHnyYq9yJMS7C+8ZzD6BvBqdKPcMX4dzpXhCt/vQUxhK08c+m5imW'
              '/Z9y1rS7c=',
    # cookie自行替换
    'cookie': 'SUV=00CE0A843DA439A25F619514603E4790; SUID=A239A43D2B12960A000000005F619515; ssuid=5385434296; '
              'SMYUV=1647951672145728; ld=WZllllllll20Fx2@lllllp2G9TDllllltDp2dZllll9lllll9llll5@@@@@@@@@@; '
              'LSTMV=346%2C311; LCLKINT=2404; ABTEST=0|1667048492|v17; SNUID=27840898EBEE06C113D4B3D2EB0EBC38; '
              'IPLOC=CN3310; wuid=1667048492920; FQV=ddceff74d09eaec5c844adefbb227470; '
              'translate.sess=5345c69c-1998-40d5-9d80-588457ed8889; SGINPUT_UPSCREEN=1667048493708 '
}

# 冷却时间
moji_cd = 1
cd = {}

# deepL功能暂不可用
catch_str = on_keyword({'sg翻'})


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
            src_lang = 'ja'
            tgt_lang = 'zh-CHS'
        elif cmd == '日 ':
            src_lang = 'zh-CHS'
            tgt_lang = 'ja'
        else:
            msg = "[CQ:at,qq={}]".format(id) + '\n命令类型错误，目前仅支持 日翻中和中翻日\n命令：【sg翻日 这样】'
            await catch_str.finish(Message(f'{msg}'))
            return
    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + '\n命令错误，目前仅支持 日翻中和中翻日\n命令：【sg翻日 这样】'
        await catch_str.finish(Message(f'{msg}'))
        return

    json1 = await get_info(src_lang, tgt_lang, text)
    nonebot.logger.info(json1)
    if json1 == "error":
        msg = "[CQ:at,qq={}]".format(id) + '\n接口返回错误，翻译失败（翻訳失敗）喵'
        await catch_str.finish(Message(f'{msg}'))
        return

    try:
        msg = "[CQ:at,qq={}]".format(id) + "\n" + json1['data']['translate']['dit']
        await catch_str.finish(Message(f'{msg}'))
    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + '\n接口返回错误，翻译失败（翻訳失敗）'
        await catch_str.finish(Message(f'{msg}'))


async def get_info(src_lang, tgt_lang, text):
    API_URL = 'https://fanyi.sogou.com/api/transpc/text/result'
    # json传参不确定是否长期有效
    json1_str = '{"from":"' + src_lang + '","to":"' + tgt_lang + '","text":"' + text + '","client":"pc","fr":"browser_pc","needQc":1,"s":"656a4135181eee8ffb80a43852f94406","uuid":"51a9a78b-7951-4f9a-8a23-64a565189096","exchange":false}'
    json1 = json.loads(json1_str)
    # json1 = {"from": src_lang, "to": tgt_lang, "text": text, "client": "pc", "fr": "browser_pc", "needQc": 1,
    #          "s": "cfd55da093a556f1d68560bc1b52e53b", "uuid": "51a9a78b-7951-4f9a-8a23-64a565189096", "exchange": False}
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
