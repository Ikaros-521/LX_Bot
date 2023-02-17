import re, datetime
import nonebot
import aiohttp
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.params import CommandArg


from nonebot.plugin import PluginMetadata


help_text = f"""
插件功能：
/查 昵称关键词或uid(uid需要以:或：或uid:或UID:或uid：打头)

""".strip()

__plugin_meta__ = PluginMetadata(
    name = 'b站转盘解析',
    description = '解析b站转盘的id和中奖列表',
    usage = help_text
)

# 请求头
header1 = {
    'content-type': 'text/plain; charset=utf-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
}

catch_str = on_command("转盘解析")


@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    # try:
        # 传入url获取sid
    sid = await get_sid(content)
    # 获取sid失败
    if sid == None:
        msg = '\n获取链接：' + content + ' 的sid失败。'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    # 获取中奖列表
    data_json = await get_win_list(sid)
    # 没有直播间 默认为0
    if data_json["code"] == 0:
        msg = "\nsid: " + sid + "\n"

        for data in data_json["data"]:
            # print(data)
            msg += "\n" + data["name"] + "  " + data["gift_name"] + "  " + await timestamp_to_date(data["ctime"])
    else:
        msg = "\n解析异常，请查看后台日志。Error Code=" + str(data_json["code"])
    
    await catch_str.finish(Message(f'{msg}'), at_sender=True)
    # except Exception as e:
    #     nonebot.logger.info(e)
    #     msg = "\n请求或解析异常，请查看后台日志"
    #     await catch_str.finish(Message(f'{msg}'), at_sender=True)


# 传入链接解析
async def get_sid(url):
    try:
        API_URL = url
        async with aiohttp.ClientSession(headers=header1) as session:
            async with session.get(url=API_URL, headers=header1) as response:
                result = await response.read()
                # print(result)
                result = result.decode('utf-8')
                match = re.search(r'newLottery_(.*?)"', result)

                if match:
                    # print(match.group(1))
                    return "newLottery_" + match.group(1)
                else:
                    return None
    except:
        return None
    

# 获取中奖列表
async def get_win_list(sid):
    try:
        if sid == None:
            return None
            
        API_URL = "https://api.bilibili.com/x/lottery/win/list?sid=" + sid
        async with aiohttp.ClientSession(headers=header1) as session:
            async with session.get(url=API_URL, headers=header1) as response:
                if response.status != 200:
                    response.raise_for_status()
                ret = await response.json()
                # print(ret)

                return ret
    except:
        return None


# 时间戳转换
async def timestamp_to_date(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    # print(dt_str)
    return dt_str  # 2021-11-09 09:46:48
