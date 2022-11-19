from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import requests

from .data import DATA

catch_str = on_keyword({'/查 '})

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
    content = get_msg[3:]

    # uid检索完成的标志位
    flag = 0

    # 遍历本地DATA
    for i in range(len(DATA)):
        # 本地匹配到结果 就直接使用本地的(由于DATA源自https://api.vtbs.moe/v1/short，可能有空数据，需要异常处理下）
        try:
            if content == DATA[i]["uname"]:
                content = str(DATA[i]["mid"])
                flag = 1
                break
        except (KeyError, TypeError, IndexError) as e:
            continue

    # 本地没有匹配到，则从b站搜索
    if flag != 1:
        # 通过昵称查询uid，默认只查搜索到的第一个用户
        info_json = await use_name_get_uid(content)
        # nonebot.logger.info(info_json)

        try:
            result = info_json['data']['result']
            # 只获取第一个搜索结果的数据
            content = str(result[0]["mid"])
        except (KeyError, TypeError, IndexError) as e:
            nonebot.logger.info("查询不到用户名为：" + content + " 的相关信息")

    # 传入uid获取用户基本信息
    base_info_json = await get_base_info(content)
    # 获取用户信息失败
    if base_info_json['code'] != 0:
        msg = "[CQ:at,qq={}]".format(id) + '\n获取uid：' + content + '，用户信息失败'
        await catch_str.finish(Message(f'{msg}'))
        return
    # 获取用户直播间id
    room_id = await get_room_id(content)
    # 没有直播间 默认为0
    if room_id == 0:
        guard_info_json = {"data": {"info": {"num": 0}}}
    else:
        guard_info_json = await get_guard_info(content, room_id)

    msg = "[CQ:at,qq={}]".format(id) + '\n用户名：' + base_info_json['card']['name'] + '\nUID：' + str(base_info_json['card']['mid']) + \
          '\n房间号：' + str(room_id) + '\n粉丝数：' + str(base_info_json['card']['fans']) + '\n舰团数：' + str(guard_info_json['data']['info']['num'])
    await catch_str.finish(Message(f'{msg}'))


# 传入uid获取用户基本信息
async def get_base_info(uid):
    API_URL = 'https://account.bilibili.com/api/member/getCardByMid?mid=' + uid
    ret = requests.get(API_URL)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret


# 传入uid获取用户直播间房间号
async def get_room_id(uid):
    API_URL = 'https://api.live.bilibili.com/room/v2/Room/room_id_by_uid?uid=' + uid
    ret = requests.get(API_URL)
    ret = ret.json()
    try:
        room_id = ret['data']['room_id']
    except TypeError:
        return 0
    return room_id


# 获取舰团信息
async def get_guard_info(uid, room_id):
    API_URL = 'https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid=' + str(room_id) + '&page=1&ruid=' + uid + '&page_size=0'
    ret = requests.get(API_URL)
    ret = ret.json()
    return ret


# 通过昵称查询信息
async def use_name_get_uid(name):
    API_URL = 'https://api.bilibili.com/x/web-interface/search/type?page_size=10&keyword=' + name + \
              '&search_type=bili_user'
    ret = requests.get(API_URL, headers=header1)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret