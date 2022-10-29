from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import requests
from nonebot_plugin_imageutils import Text2Image
from io import BytesIO
import time

catch_str = on_keyword({'/查直播 '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    id = event.get_user_id()
    # nonebot.logger.info(get_msg)
    content = get_msg[5:]

    # 以空格分割 用户uid 最近n场
    content = content.split()
    src_uid = ""
    info_size = "99999"

    if len(content) == 1:
        src_uid = content[0]
    elif len(content) > 1:
        src_uid = content[0]
        info_size = content[1]
    else:
        msg = "[CQ:at,qq={}]".format(id) + '传参错误，命令格式【/查直播 用户uid 最近场次数】'
        await catch_str.finish(Message(f'{msg}'))
        return

    # 数组中存放你想要快速匹配的用户，对应其uid填入uids数组
    name = ['火羽', '猫雷', '莉爱', '雫酱', 'lulu', 'neol', 'koni']
    uid = ['2094031249', '697091119', '1485277312', '1602464609', '387636363', '1300421811', '1372936974']
    try:
        index = name.index(src_uid)
    except ValueError:
        index = -1
    # print(index)

    if index != -1:
        src_uid = uid[index]

    info_json = await get_info(src_uid)

    # 判断返回代码
    if info_json['code'] != 200:
        msg = "[CQ:at,qq={}]".format(id) + '查询用户：' + content + '失败'
        await catch_str.finish(Message(f'{msg}'))
        return

    out_str = " 昵称:" + info_json["data"]["channel"]["name"] + "  UID:" + src_uid + "  房间号:" + \
              str(info_json["data"]["channel"]["roomId"]) + "\n 总直播数：" + \
              str(info_json["data"]["channel"]["totalLiveCount"]) + \
              " 总弹幕数:" + str(info_json["data"]["channel"]["totalDanmakuCount"]) + " 总收益:￥" + \
              str(info_json["data"]["channel"]["totalIncome"]) + \
              " 总直播时长:" + str(round(info_json["data"]["channel"]["totalLiveSecond"] / 60 / 60, 2)) + "h\n" + \
              " 显示格式为: 结束时间 | 标题 | 弹幕数 | 观看数 | 互动数 | 总收益\n"

    for i in range(len(info_json["data"]["lives"])):
        # 达到指定数量场次
        if i == int(info_size):
            break
        out_str += "{:<s} | {:<s} | {:<d} | {:<d} | {:<d} | ￥{:<.1f}".format(
            await timestamp_to_date(info_json["data"]["lives"][i]["stopDate"]),
            info_json["data"]["lives"][i]["title"],
            info_json["data"]["lives"][i]["danmakusCount"],
            info_json["data"]["lives"][i]["watchCount"],
            info_json["data"]["lives"][i]["interactionCount"],
            info_json["data"]["lives"][i]["totalIncome"])
        out_str += '\n'
        # 2000场就算了吧，太多了
        if i >= 2000:
            break
    # nonebot.logger.info("\n" + out_str)

    if len(info_json["data"]["lives"]) < 2000:
        # img: PIL.Image.Image
        img = Text2Image.from_text(out_str, 30, align="left", fill="green", fontname="Microsoft YaHei").to_image()

        # 以上结果为 PIL 的 Image 格式，若要直接 MessageSegment 发送，可以转为 BytesIO
        output = BytesIO()
        img.save(output, format="png")
        await catch_str.send(MessageSegment.image(output))
    else:
        id = event.get_user_id()
        msg = "[CQ:at,qq={}]".format(id) + '果咩，直播数大于2000，发不出去喵~'
        await catch_str.finish(Message(f'{msg}'))


async def get_info(uid):
    API_URL = 'https://danmaku.suki.club/api/info/channel?cid=' + uid
    ret = requests.get(API_URL, verify=False)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret


# 将13位时间戳转换为时间字符串，默认为2017/11/01 11:11:01格式
async def timestamp_to_date(time_stamp, format_string="%Y/%m/%d %H:%M:%S"):
    time_array = time.localtime(int(time_stamp / 1000))
    str_date = time.strftime(format_string, time_array)
    return str_date
