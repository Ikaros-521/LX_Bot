from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import requests
from nonebot_plugin_imageutils import Text2Image
from io import BytesIO


catch_str = on_keyword({'/查成分 观看 '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[8:]

    # 数组中存放你想要快速匹配的用户，对应其uid填入uids数组
    name = ['火羽', '猫雷', '莉爱', '雫酱', 'lulu', 'neol', 'koni', 'naru']
    uid = ['2094031249', '697091119', '1485277312', '1602464609', '387636363', '1300421811', '1372936974', '1354255177']
    try:
        index = name.index(content)
    except ValueError:
        index = -1
    # print(index)

    if index != -1:
        content = uid[index]

    user_info_json = await get_user_info(content)

    # 判断返回代码
    if user_info_json['code'] != 200:
        id = event.get_user_id()
        msg = "[CQ:at,qq={}]".format(id) + '查询用户：' + content + '失败'
        await catch_str.finish(Message(f'{msg}'))
        return

    out_str = " 查询用户UID：" + content + "\n" + \
              " 显示格式为：【 昵称 】 UID | 房间号\n"
    # 数据集合
    name_set = set()
    uId_set = set()
    roomId_set = set()

    for i in range(len(user_info_json['data'])):
        name = user_info_json['data'][i]['name']
        uId = user_info_json['data'][i]['uId']
        roomId = user_info_json['data'][i]['roomId']

        name_set.add(name)
        uId_set.add(uId)
        roomId_set.add(roomId)

    name_list = list(name_set)
    uId_list = list(uId_set)
    roomId_list = list(roomId_set)

    out_str += " 观看总数：" + str(len(uId_set)) + "\n"

    for i in range(len(uId_set)):
        out_str += "【 {:<s} 】 {:<d} | {:<d}".format(name_list[i], uId_list[i], roomId_list[i])
        out_str += '\n'
    # nonebot.logger.info("\n" + out_str)

    if len(uId_set) < 1000:
        # img: PIL.Image.Image
        img = Text2Image.from_text(out_str, 35, align="left", fill="green", fontname="Microsoft YaHei").to_image()

        # 以上结果为 PIL 的 Image 格式，若要直接 MessageSegment 发送，可以转为 BytesIO
        output = BytesIO()
        img.save(output, format="png")
        await catch_str.send(MessageSegment.image(output))
    else:
        id = event.get_user_id()
        msg = "[CQ:at,qq={}]".format(id) + '果咩，dd数大于1000，发不出去喵~'
        await catch_str.finish(Message(f'{msg}'))


async def get_user_info(uid):
    API_URL = 'https://danmaku.suki.club/api/search/user/channel?uid=' + uid
    ret = requests.get(API_URL, verify=False)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret
