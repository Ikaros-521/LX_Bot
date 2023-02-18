import nonebot
# from io import BytesIO
from nonebot import on_keyword, on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.params import CommandArg
import aiohttp, json


from nonebot.plugin import PluginMetadata


help_text = f"""
插件功能：
/缘分 小白 小红
/缘分测试 黑 白

传入2个人的名字，返回缘分测试的结果

""".strip()

__plugin_meta__ = PluginMetadata(
    name = '缘分测试',
    description = '适用于nonebot2 v11的缘分测试工具',
    usage = help_text
)


# 所有的命令都在这哦，要改命令触发关键词的请自便
catch_str = on_command("缘分", aliases={"缘分测试"})

# 
@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    content = content.split()

    name1 = ""
    name2 = ""

    if len(content) > 1:
        name1 = content[0]
        name2 = content[1]
    else:
        msg = '\n命令错误，例如：【/缘分 大熊 静香】'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    try:
        msg = await get_data(name1, name2)
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data(name1, name2):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/yf.php?name1=' + name1 + '&name2=' + name2
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')
