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

# data文件有依赖性，如果单独装，请替换下
from .nonebot_plugin_searchBiliInfo.data import DATA

catch_str = on_keyword({'/查收益 '})

# 请求头贴入你的b站cookie
header1 = {
    'cookie': 'buvid3=52D30BB7-20FB-C7BA-60B7-EB3F18A8EB9C62437infoc; b_nut=1662632862; i-wanna-go-back=-1; b_ut=5; '
              '_uuid=FB5921023-4BF10-D48E-10A62-EE619E5FA65E60948infoc; buvid_fp=3b2946a9aa52740147f7478c79476df7; '
              'buvid4=0068E57C-9762-7898-4F73-0B8994558CF463776-022090818-FRmBv7s/ltnMkEnT97AnUQ%3D%3D; '
              'fingerprint=eac7b07cd79cd55526b5a7206425ddc6; buvid_fp_plain=undefined; '
              'SESSDATA=89e822a8%2C1678184893%2Cb9824%2A91; bili_jct=3d33d52161227b9ec082ba6124be8d63; '
              'DedeUserID=1123180192; DedeUserID__ckMd5=6b55cc0fe28987d3; sid=8m93076x; PVID=25; '
              'LIVE_BUVID=AUTO9316626329021634; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1663557853,1663637087,'
              '1663811728,1663935967; bp_video_offset_1123180192=707172485766840300; b_lsid=338EE34E_1836A5BC399; '
              '_dfcaptcha=62ba3e19085f0e3de59bc4dcf7663756; innersign=0; '
              'Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1663937476 '
}

@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    id = event.get_user_id()
    # nonebot.logger.info(get_msg)
    content = get_msg[5:]

    # 以空格分割 用户uid 收益类型(默认1: 礼物，2: 上舰，3: SC) 倒叙第n场(从0开始)
    content = content.split()
    src_uid = ""
    live_index = "0"
    income_type = "1"

    if len(content) == 1:
        src_uid = content[0]
    elif len(content) == 2:
        src_uid = content[0]
        income_type = content[1]
    elif len(content) > 2:
        src_uid = content[0]
        income_type = content[1]
        live_index = content[2]
    else:
        msg = "[CQ:at,qq={}]".format(id) + '传参错误，命令格式【/查直播 收益类型(默认1: 礼物，2: 上舰，3: SC) 用户uid 倒叙第n场(从0开始)】'
        await catch_str.finish(Message(f'{msg}'))
        return

    # uid检索完成的标志位
    flag = 0

    # 遍历本地DATA
    for i in range(len(DATA)):
        # 本地匹配到结果 就直接使用本地的(由于DATA源自https://api.vtbs.moe/v1/short，可能有空数据，需要异常处理下）
        try:
            if content == DATA[i]["uname"]:
                src_uid = str(DATA[i]["mid"])
                flag = 1
                break
        except (KeyError, TypeError, IndexError) as e:
            continue

    # 本地没有匹配到，则从b站搜索
    if flag != 1:
        # 通过昵称查询uid，默认只查搜索到的第一个用户
        info_json = await use_name_get_uid(src_uid)
        # nonebot.logger.info(info_json)

        try:
            result = info_json['data']['result']
            # 只获取第一个搜索结果的数据
            src_uid = str(result[0]["mid"])
        except (KeyError, TypeError, IndexError) as e:
            nonebot.logger.info("查询不到用户名为：" + src_uid + " 的相关信息")

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

    # 默认1: 礼物，2: 上舰，3: SC
    if income_type == "礼物":
        income_type = "1"
    elif income_type == "上舰":
        income_type = "2"
    elif income_type == "SC" | income_type == "sc" | income_type == "Sc":
        income_type = "3"
    else:
        income_type = "1"

    # nonebot.logger.info(out_str + "income_type:" + income_type)

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


# 通过昵称查询信息
async def use_name_get_uid(name):
    API_URL = 'https://api.bilibili.com/x/web-interface/search/type?page_size=10&keyword=' + name + \
              '&search_type=bili_user'
    ret = requests.get(API_URL, headers=header1)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret


# 将13位时间戳转换为时间字符串，默认为2017/11/01 11:11:01格式
async def timestamp_to_date(time_stamp, format_string="%Y/%m/%d %H:%M:%S"):
    time_array = time.localtime(int(time_stamp / 1000))
    str_date = time.strftime(format_string, time_array)
    return str_date
