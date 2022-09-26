from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import requests

catch_str = on_keyword({'/查昵称 '})

header1 = {
    # 要使用此功能，请加入填入你的cookie
    'cookie': ''
}

@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[5:]

    info_json = await get_info(content)
    # nonebot.logger.info(info_json)

    id = event.get_user_id()

    try:
        result = info_json['data']['result']
    except KeyError:
        msg = "[CQ:at,qq={}]".format(id) + ' 查询无结果'
        await catch_str.finish(Message(f'{msg}'))
        return

    msg = "[CQ:at,qq={}]".format(id) + "\n 查询用户名：" + content + "\n" + \
          " 显示格式为：【 UID  昵称  粉丝数 】\n"
    for i in range(len(result)):
        msg += " 【 " + str(result[i]["mid"]) + "  " + result[i]["uname"] + "  " + str(result[i]["fans"]) + ' 】\n'
    await catch_str.finish(Message(f'{msg}'))


async def get_info(name):
    API_URL = 'https://api.bilibili.com/x/web-interface/search/type?page_size=10&keyword=' + name + \
              '&search_type=bili_user'
    ret = requests.get(API_URL, headers=header1)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret
