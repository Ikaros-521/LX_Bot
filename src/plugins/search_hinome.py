import json

import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword, require
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import time

require("nonebot_plugin_htmlrender")

from nonebot_plugin_htmlrender import (
    text_to_pic,
    md_to_pic,
    template_to_pic,
    get_new_page,
)


# 请求头贴入你的b站cookie
header1 = {
    'content-type': 'text/plain; charset=utf-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
}

catch_str = on_keyword({'/查火羽'}, priority=1)


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = '2094031249'

    base_info_json = await get_base_info(content)
    room_id = await get_room_id(content)
    guard_info_json = await get_guard_info(content, room_id)

    msg = '\n用户名：' + base_info_json['card']['name'] + '\nUID：' + str(base_info_json['card']['mid']) + \
          '\n房间号：' + str(room_id) + '\n粉丝数：' + str(base_info_json['card']['fans']) + '\n舰团数：' + str(guard_info_json['data']['info']['num'])
    
    info_json = await get_info(content)

    try:
        # 判断返回代码
        if info_json['code'] != 200:
            msg += '\n查询用户：' + content + '失败'
            await catch_str.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        msg += '\n查询用户：' + content + '失败'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    out_str = "#查直播\n\n昵称:" + info_json["data"]["channel"]["name"] + "  UID:" + content + "  房间号:" + \
              str(info_json["data"]["channel"]["roomId"]) + "\n\n 总直播数:" + \
              str(info_json["data"]["channel"]["totalLiveCount"]) + \
              "  总弹幕数:" + str(info_json["data"]["channel"]["totalDanmakuCount"]) + "  总收益:￥" + \
              str(info_json["data"]["channel"]["totalIncome"]) + \
              "  总直播时长:" + str(round(info_json["data"]["channel"]["totalLiveSecond"] / 60 / 60, 2)) + "h\n\n" + \
              "| 开始时间 | 时长 | 标题 | 弹幕数 | 观看数 | 互动数 | 总收益 |\n" \
              "| :-----| :-----| :-----| :-----| :-----| :-----| :-----|\n"

    for i in range(len(info_json["data"]["lives"])):
        # 达到指定数量场次
        if i == 3:
            break
        try:
            if info_json["data"]["lives"][i]["stopDate"] is None:
                out_str += "| {:<s} | 直播中 | {:<s} | {:<d} | {:<d} | {:<d} | ￥{:<.1f} |".format(
                    await timestamp_to_date(info_json["data"]["lives"][i]["startDate"]),
                    info_json["data"]["lives"][i]["title"],
                    info_json["data"]["lives"][i]["danmakusCount"],
                    info_json["data"]["lives"][i]["watchCount"],
                    info_json["data"]["lives"][i]["interactionCount"],
                    info_json["data"]["lives"][i]["totalIncome"])
            else:
                out_str += "| {:<s} | {:<.2f}h | {:<s} | {:<d} | {:<d} | {:<d} | ￥{:<.1f} |".format(
                    await timestamp_to_date(info_json["data"]["lives"][i]["startDate"]),
                    (info_json["data"]["lives"][i]["stopDate"] - info_json["data"]["lives"][i][
                        "startDate"]) / 1000 / 3600,
                    info_json["data"]["lives"][i]["title"],
                    info_json["data"]["lives"][i]["danmakusCount"],
                    info_json["data"]["lives"][i]["watchCount"],
                    info_json["data"]["lives"][i]["interactionCount"],
                    info_json["data"]["lives"][i]["totalIncome"])
        except (KeyError, TypeError, IndexError) as e:
            out_str += "| {:<s} | 直播中 | {:<s} | {:<d} | {:<d} | {:<d} | ￥{:<.1f} |".format(
                await timestamp_to_date(info_json["data"]["lives"][i]["startDate"]),
                info_json["data"]["lives"][i]["title"],
                info_json["data"]["lives"][i]["danmakusCount"],
                info_json["data"]["lives"][i]["watchCount"],
                info_json["data"]["lives"][i]["interactionCount"],
                info_json["data"]["lives"][i]["totalIncome"])
        out_str += '\n'
        # 2000场就算了吧，太多了
        if i >= 2000:
            break
    out_str += '\n数据源自：danmakus.com\n'
    # nonebot.logger.info("\n" + out_str)

    if len(info_json["data"]["lives"]) < 2000:
        output = await md_to_pic(md=out_str, width=1000)
        await catch_str.send(MessageSegment.text(msg) + MessageSegment.image(output))
    else:
        msg += '果咩，直播数大于2000，发不出去喵~'
        await catch_str.finish(MessageSegment.text(msg), at_sender=True)


async def get_info(uid):
    try:
        API_URL = 'https://danmakus.com/api/info/channel?cid=' + uid
        async with aiohttp.ClientSession(headers=header1) as session:
            async with session.get(url=API_URL, headers=header1) as response:
                ret = await response.json()
    except Exception as e:
        # nonebot.logger.info(e)
        return {"code": 408}
    nonebot.logger.info(ret)
    return ret


async def get_base_info(uid):
    API_URL = 'https://account.bilibili.com/api/member/getCardByMid?mid=' + uid
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret


async def get_room_id(uid):
    API_URL = 'https://api.live.bilibili.com/room/v2/Room/room_id_by_uid?uid=' + uid
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    room_id = ret['data']['room_id']
    return room_id


async def get_guard_info(uid, room_id):
    API_URL = 'https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid=' + str(room_id) + '&page=1&ruid=' + uid + '&page_size=0'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    return ret


async def timestamp_to_date(timestamp):
    # 转换成localtime
    time_local = time.localtime(timestamp / 1000)
    # 转换成新的时间格式(精确到秒)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt  # 2021-11-09 09:46:48
