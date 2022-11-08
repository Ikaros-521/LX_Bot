from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import requests
from nonebot_plugin_imageutils import Text2Image
from io import BytesIO
import time
from nonebot_plugin_htmlrender import (
    text_to_pic,
    md_to_pic,
    template_to_pic,
    get_new_page,
)

catch_str = on_keyword({'/查收益 '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    id = event.get_user_id()
    # nonebot.logger.info(get_msg)
    content = get_msg[5:]

    # 以空格分割 用户uid 倒叙第n场(从0开始) 收益类型(默认1: 礼物，2: 上舰，3: SC)
    content = content.split()
    src_uid = ""
    live_index = "0"
    income_type = "1"

    if len(content) == 1:
        src_uid = content[0]
    elif len(content) == 2:
        src_uid = content[0]
        live_index = content[1]
    elif len(content) > 2:
        src_uid = content[0]
        live_index = content[1]
        income_type = content[2]
    else:
        msg = "[CQ:at,qq={}]".format(id) + '传参错误，命令格式【/查直播 用户uid 倒叙第n场(从0开始) 收益类型(默认1: 礼物，2: 上舰，3: SC)】'
        await catch_str.finish(Message(f'{msg}'))
        return

    # 数组中存放你想要快速匹配的用户，对应其uid填入uids数组
    name = ['火羽', '猫雷', '莉爱', '雫酱', 'lulu', 'neol', 'koni', 'naru', '羽月']
    uid = ['2094031249', '697091119', '1485277312', '1602464609', '387636363', '1300421811', '1372936974', '1354255177',
           '1682889553']
    try:
        index = name.index(src_uid)
    except ValueError:
        index = -1
    # print(index)

    if index != -1:
        src_uid = uid[index]

    live_json = await get_live_info(src_uid)

    # 判断返回代码
    if live_json['code'] != 200:
        msg = "[CQ:at,qq={}]".format(id) + '查询用户：' + src_uid + ' 直播信息失败'
        await catch_str.finish(Message(f'{msg}'))
        return

    try:
        live_id = live_json['data']['lives'][int(live_index)]['liveId']
        username = live_json["data"]["channel"]["name"]
        room_id = str(live_json["data"]["channel"]["roomId"])
        totalLiveCount = str(live_json["data"]["channel"]["totalLiveCount"])
        totalDanmakuCount = str(live_json["data"]["channel"]["totalDanmakuCount"])
        totalIncome = str(live_json["data"]["channel"]["totalIncome"])
        totalLivehour = str(round(live_json["data"]["channel"]["totalLiveSecond"] / 60 / 60, 2))

    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + '查询用户：' + src_uid + '失败,live_id解析失败,可能原因：场次数不对；无此场次'
        await catch_str.finish(Message(f'{msg}'))
        return

    out_str = "#查收益\n\n昵称:" + username + "  UID:" + src_uid + "  房间号:" + room_id + "\n\n 总直播数:" + \
              totalLiveCount + "  总弹幕数:" + totalDanmakuCount + "  总收益:￥" + totalIncome + \
              "  总直播时长:" + totalLivehour + "h\n\n" + \
              "| 时间 | uid | 昵称 | 内容 | 价格|\n" \
              "| :-----| :-----| :-----| :-----| :-----|\n"

    # 获取当场直播信息
    info_json = await get_info(live_id, income_type)
    if info_json['code'] != 200:
        msg = "[CQ:at,qq={}]".format(id) + '查询用户：' + src_uid + ' 场次数据失败'
        await catch_str.finish(Message(f'{msg}'))
        return

    # 遍历弹幕信息
    for i in range(len(info_json["data"]["danmakus"])):
        out_str += "| {:<s} | {:<d} | {:<s} | {:<s} | ￥{:<.1f} |".format(
            await timestamp_to_date(info_json["data"]["danmakus"][i]["sendDate"]),
            info_json["data"]["danmakus"][i]["uId"],
            info_json["data"]["danmakus"][i]["name"],
            info_json["data"]["danmakus"][i]["message"],
            info_json["data"]["danmakus"][i]["price"])
        out_str += '\n'
        # 2000条就算了吧，太多了
        if i >= 2000:
            break
    # nonebot.logger.info("\n" + out_str)

    if len(info_json["data"]["danmakus"]) < 2000:
        output = await md_to_pic(md=out_str, width=1000)
        await catch_str.send(MessageSegment.image(output))
    else:
        id = event.get_user_id()
        msg = "[CQ:at,qq={}]".format(id) + '果咩，礼物数大于2000，发不出去喵~'
        await catch_str.finish(Message(f'{msg}'))


async def get_live_info(uid):
    API_URL = 'https://danmaku.suki.club/api/info/channel?cid=' + uid
    ret = requests.get(API_URL, verify=False)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret


async def get_info(live_id, income_type):
    API_URL = 'https://danmaku.suki.club/api/info/live?liveid=' + live_id + '&type=' + income_type + '&uid='
    ret = requests.get(API_URL, verify=False)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret


# 将13位时间戳转换为时间字符串，默认为2017/11/01 11:11:01格式
async def timestamp_to_date(time_stamp, format_string="%Y/%m/%d %H:%M:%S"):
    time_array = time.localtime(int(time_stamp / 1000))
    str_date = time.strftime(format_string, time_array)
    return str_date
