from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random
from nonebot_plugin_imageutils import Text2Image
from io import BytesIO
import requests

catch_str = on_keyword({'/查舰团 '})


@catch_str.handle()
async def send_img(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[5:]

    # 数组中存放你想要快速匹配的用户，对应其uid填入uids数组
    name = ['火羽', '猫雷', '莉爱', '雫酱', 'lulu', 'neol', 'koni', 'naru', '羽月']
    uid = ['2094031249', '697091119', '1485277312', '1602464609', '387636363', '1300421811', '1372936974', '1354255177',
           '1682889553']
    try:
        index = name.index(content)
    except ValueError:
        index = -1
    # print(index)

    if index != -1:
        content = uid[index]

    guard_info_json = await get_user_guard(content)

    out_str = " 查询用户UID：" + content + "\n" + \
              " 显示格式为：【 昵称 】 【 UID 】 【 舰团类型 】\n"
    for i in range(len(guard_info_json)):
        uname = guard_info_json[i]['uname']
        mid = guard_info_json[i]['mid']
        if guard_info_json[i]['level'] == 0:
            level = '总督'
        elif guard_info_json[i]['level'] == 1:
            level = '提督'
        else:
            level = '舰长'
        out_str += "【 {:<s} 】 【 {:<d} 】 【 {:<s} 】".format(uname, mid, level)
        out_str += '\n'
    # nonebot.logger.info("\n" + out_str)

    # img: PIL.Image.Image
    img = Text2Image.from_text(out_str, 35, align="left", fill="green", fontname="Microsoft YaHei").to_image()

    # 以上结果为 PIL 的 Image 格式，若要直接 MessageSegment 发送，可以转为 BytesIO
    output = BytesIO()
    img.save(output, format="png")
    await catch_str.send(MessageSegment.image(output))


async def get_user_guard(uid):
    API_URL = 'https://api.tokyo.vtbs.moe/v1/guard/' + uid
    ret = requests.get(API_URL)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret


def get_CNStr_lens(needlen, String):
    ret1 = len(String.encode("GBK")) - len(String)
    return needlen - int(ret1 * 3 / 3)


def size_change(str1):
    lenStr = len(str1)
    #　nonebot.logger.info("lenStr=" + str(lenStr))
    lenStr_utf8 = len(str1.encode('utf-8'))
    # nonebot.logger.info("lenStr_utf8=" + str(lenStr_utf8))
    lenStr_gbk = len(str1.encode('GBK'))
    # nonebot.logger.info("lenStr_utf8=" + str(lenStr_utf8))
    size_3 = int((lenStr_utf8 - lenStr) / 2)
    size_2 = lenStr - size_3
    size = size_3 * 3 + size_2
    # nonebot.logger.info("size=" + str(size))
    return size_3
