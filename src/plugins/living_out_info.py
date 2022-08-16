from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import requests

catch_str = on_keyword({'/live.bilibili.com'})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    room_id = get_msg.split("/")[-1]
    # nonebot.logger.info(room_id)

    uid = await get_uid_id(room_id)
    base_info_json = await get_base_info(str(uid))
    guard_info_json = await get_guard_info(str(uid), room_id)

    id = event.get_user_id()
    msg = "[CQ:at,qq={}]".format(id) + '\n用户名：' + base_info_json['card']['name'] + '\nUID：' + str(uid) + \
          '\n房间号：' + room_id + '\n粉丝数：' + str(base_info_json['card']['fans']) + '\n舰团数：' + str(guard_info_json['data']['info']['num'])
    await catch_str.finish(Message(f'{msg}'))


async def get_base_info(uid):
    API_URL = 'https://account.bilibili.com/api/member/getCardByMid?mid=' + uid
    ret = requests.get(API_URL)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret


async def get_uid_id(room_id):
    API_URL = 'https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo?room_id=' + room_id + \
        '&protocol=0,1&format=0,1,2&codec=0,1&qn=0&platform=web&ptype=8&dolby=5&panorama=1'
    ret = requests.get(API_URL)
    ret = ret.json()
    if ret["code"] != 0:
        nonebot.logger.info(str(room_id) + "不是正确的房间号")
        return 0
    uid = ret['data']['uid']
    return uid


async def get_guard_info(uid, room_id):
    API_URL = 'https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid=' + str(room_id) + '&page=1&ruid=' + uid + '&page_size=0'
    ret = requests.get(API_URL)
    ret = ret.json()
    return ret
