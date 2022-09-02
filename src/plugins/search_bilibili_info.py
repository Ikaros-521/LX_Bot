from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import requests

catch_str = on_keyword({'/查 '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[3:]

    # 数组中存放你想要快速匹配的用户，对应其uid填入uids数组
    name = ['火羽', '猫雷', '莉爱', '雫酱', 'lulu', 'neol', 'koni']
    uid = ['2094031249', '697091119', '1485277312', '1602464609', '387636363', '1300421811', '1372936974']
    try:
        index = name.index(content)
    except ValueError:
        index = -1
    # print(index)

    if index != -1:
        content = uid[index]

    base_info_json = await get_base_info(content)
    room_id = await get_room_id(content)
    guard_info_json = await get_guard_info(content, room_id)

    id = event.get_user_id()
    msg = "[CQ:at,qq={}]".format(id) + '\n用户名：' + base_info_json['card']['name'] + '\nUID：' + str(base_info_json['card']['mid']) + \
          '\n房间号：' + str(room_id) + '\n粉丝数：' + str(base_info_json['card']['fans']) + '\n舰团数：' + str(guard_info_json['data']['info']['num'])
    await catch_str.finish(Message(f'{msg}'))


async def get_base_info(uid):
    API_URL = 'https://account.bilibili.com/api/member/getCardByMid?mid=' + uid
    ret = requests.get(API_URL)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret


async def get_room_id(uid):
    API_URL = 'https://api.live.bilibili.com/room/v2/Room/room_id_by_uid?uid=' + uid
    ret = requests.get(API_URL)
    ret = ret.json()
    room_id = ret['data']['room_id']
    return room_id


async def get_guard_info(uid, room_id):
    API_URL = 'https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid=' + str(room_id) + '&page=1&ruid=' + uid + '&page_size=0'
    ret = requests.get(API_URL)
    ret = ret.json()
    return ret
