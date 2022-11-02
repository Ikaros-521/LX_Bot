from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import requests
from io import BytesIO
from nonebot_plugin_htmlrender import (
    text_to_pic,
    md_to_pic,
    template_to_pic,
    get_new_page,
)
from nonebot.adapters.onebot.v11 import unescape
import nonebot

catch_str = on_keyword({'/营收 '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    id = event.get_user_id()
    get_msg = str(event.get_message())
    content = get_msg[4:]

    if content == '月榜':
        json1 = await get_month()
    elif content == '周榜':
        json1 = await get_week()
    elif content == '日榜':
        json1 = await get_day()
    else:
        msg = "[CQ:at,qq={}]".format(id) + '\n命令错误，例如：【/营收 月榜】【/营收 周榜】【/营收 日榜】'
        await catch_str.finish(Message(f'{msg}'))
        return

    if json1["code"] != 200:
        msg = "[CQ:at,qq={}]".format(id) + '\n请求失败，寄了喵'
        await catch_str.finish(Message(f'{msg}'))
        return

    try:
        out_str = "#VTB营收" + content + "\n" \
                                       "| 用户名 | uid | 营收 | 付费人数 | 弹幕总数 | 直播时长 |\n" \
                                       "| :-----| :-----| :-----| :-----| :-----| :-----|\n"
        for i in range(len(json1['data'])):
            name = json1['data'][i]['name']
            danmaku = json1['data'][i]['danmaku']
            gold_user = json1['data'][i]['goldUser']
            income = json1['data'][i]['income']
            mid = json1['data'][i]['mid']
            live_time = json1['data'][i]['liveTime']

            out_str += '| ' + name + ' | ' + str(mid) + ' | '
            if income > 1000000:
                income = round(income / 1000000, 2)
                out_str += str(income) + '万 | '
            else:
                income = round(income / 100, 2)
                out_str += str(income) + '元 | '
            out_str += str(gold_user) + '人 | ' + str(danmaku) + '条 | '
            live_time = round(live_time / 60 / 60, 2)
            out_str += str(live_time) + 'h |' + '\n'
        # nonebot.logger.info("\n" + out_str)

        output = await md_to_pic(md=out_str, width=800)
        # 如果需要保存到本地则去除下面2行注释
        # output = Image.open(BytesIO(img))
        # output.save("md2pic.png", format="PNG")
        await catch_str.send(MessageSegment.image(output))
    except (KeyError, TypeError, IndexError) as e:
        msg = "[CQ:at,qq={}]".format(id) + '\n数据解析失败，寄了喵'
        await catch_str.finish(Message(f'{msg}'))
        return


async def get_month():
    API_URL = 'http://www.vtbs.fun:8050/rank/income?dateRange=%E6%9C%88%E6%A6%9C&current=1&size=100'
    ret = requests.get(API_URL)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret


async def get_week():
    API_URL = 'http://www.vtbs.fun:8050/rank/income?dateRange=%E5%91%A8%E6%A6%9C&current=1&size=100'
    ret = requests.get(API_URL)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret


async def get_day():
    API_URL = 'http://www.vtbs.fun:8050/rank/income?dateRange=%E6%97%A5%E6%A6%9C&current=1&size=100'
    ret = requests.get(API_URL)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret
