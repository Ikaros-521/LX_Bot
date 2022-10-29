import datetime
import nonebot
import requests
import time
from io import BytesIO
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.typing import T_State
from nonebot_plugin_imageutils import Text2Image

catch_str = on_keyword({'/查成分 弹幕 '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[8:]

    # 以空格分割 用户uid 目标uid 页数 条数
    content = content.split()
    src_uid = ""
    tgt_uid = ""
    page = "0"
    page_size = "3"

    if len(content) > 1:
        src_uid = content[0]
        tgt_uid = content[1]
    else:
        id = event.get_user_id()
        msg = "[CQ:at,qq={}]".format(id) + '传参错误，命令格式【/查成分 弹幕 用户uid 目标uid 页数】'
        await catch_str.finish(Message(f'{msg}'))
        return

    if len(content) == 3:
        page = content[2]

    # 数组中存放你想要快速匹配的用户，对应其uid填入uids数组
    name = ['火羽', '猫雷', '莉爱', '雫酱', 'lulu', 'neol', 'koni', 'naru']
    uid = ['2094031249', '697091119', '1485277312', '1602464609', '387636363', '1300421811', '1372936974', '1354255177']
    try:
        index = name.index(content[0])
    except ValueError:
        index = -1
    # print(index)

    if index != -1:
        src_uid = uid[index]

    try:
        index = name.index(content[1])
    except ValueError:
        index = -1
    # print(index)

    if index != -1:
        tgt_uid = uid[index]

    info_json = await get_info(src_uid, tgt_uid, page, page_size)

    # 判断返回代码
    if info_json['code'] != 200:
        id = event.get_user_id()
        msg = "[CQ:at,qq={}]".format(id) + '查询出错'
        await catch_str.finish(Message(f'{msg}'))
        return

    data_len = 0
    out_str = " 查询用户UID：" + src_uid + ", 目标UID：" + tgt_uid + ", 页数：" + page + ", 条数：" + page_size + "\n" + \
              " 显示格式为：【 时间 】 内容\n"
    for i in range(len(info_json['data']['data'])):
        title = info_json['data']['data'][i]['live']['title']
        out_str += '\n 标题：' + title + '\n'
        for j in range(len(info_json['data']['data'][i]['danmakus'])):
            date = await timestamp_to_date(info_json['data']['data'][i]['danmakus'][j]['sendDate'])
            message = info_json['data']['data'][i]['danmakus'][j]['message']
            out_str += '【' + str(date) + '】 ' + message + '\n'
            data_len += 1
    # nonebot.logger.info("\n" + out_str)

    if data_len < 1000:
        # img: PIL.Image.Image
        img = Text2Image.from_text(out_str, 35, align="left", fill="green", fontname="Microsoft YaHei").to_image()

        # 以上结果为 PIL 的 Image 格式，若要直接 MessageSegment 发送，可以转为 BytesIO
        output = BytesIO()
        img.save(output, format="png")
        await catch_str.send(MessageSegment.image(output))
    else:
        id = event.get_user_id()
        msg = "[CQ:at,qq={}]".format(id) + '果咩，弹幕数大于1000，发不出去喵~'
        await catch_str.finish(Message(f'{msg}'))


async def get_info(src_uid, tgt_uid, page, page_size):
    API_URL = 'https://danmaku.suki.club/api/search/user/detail?uid=' + src_uid + '&target=' + tgt_uid + \
              '&pagenum=' + page + '&pagesize=' + page_size
    ret = requests.get(API_URL, verify=False)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret


async def timestamp_to_date(timestamp):
    # 转换成localtime
    time_local = time.localtime(timestamp / 1000)
    # 转换成新的时间格式(精确到秒)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt  # 2021-11-09 09:46:48
