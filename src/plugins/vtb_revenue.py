from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import requests
from io import BytesIO
from nonebot_plugin_imageutils import Text2Image

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
        out_str = " VTB营收" + content + "\n 显示格式为：用户名 | uid | 营收 | 付费人数 | 弹幕总数 | 直播时长\n\n"
        for i in range(len(json1['data'])):
            name = json1['data'][i]['name']
            danmaku = json1['data'][i]['danmaku']
            gold_user = json1['data'][i]['goldUser']
            income = json1['data'][i]['income']
            mid = json1['data'][i]['mid']
            live_time = json1['data'][i]['liveTime']

            out_str += ' ' + name + ' | ' + str(mid) + ' | '
            if income > 1000000:
                income = round(income / 1000000, 2)
                out_str += str(income) + '万 | '
            else:
                income = round(income / 100, 2)
                out_str += str(income) + '元 | '
            out_str += str(gold_user) + '人 | ' + str(danmaku) + '条 | '
            live_time = round(live_time / 60 / 60, 2)
            out_str += str(live_time) + 'h ' + '\n'
        # nonebot.logger.info("\n" + out_str)

        # img: PIL.Image.Image
        img = Text2Image.from_text(out_str, 35, align="left", fill="green", fontname="Microsoft YaHei").to_image()

        # 以上结果为 PIL 的 Image 格式，若要直接 MessageSegment 发送，可以转为 BytesIO
        output = BytesIO()
        img.save(output, format="png")
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
