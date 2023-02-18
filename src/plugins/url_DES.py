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
/url编码 传入内容
/URL编码 传入内容
/url解码 传入内容
/URL解码 传入内容

对URL进行编解码

""".strip()

__plugin_meta__ = PluginMetadata(
    name = 'URL编解码',
    description = '适用于nonebot2 v11的URL编解码',
    usage = help_text
)


# 所有的命令都在这哦，要改命令触发关键词的请自便
catch_str = on_command("url编码", aliases={"URL编码"})
catch_str2 = on_command("url解码", aliases={"URL解码"})


@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    try:
        msg = await get_data(content)
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


@catch_str2.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    try:
        msg = await get_data(content, 1)
        await catch_str2.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str2.finish(Message(f'{msg}'), at_sender=True)


async def get_data(msg, type=None):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/url.php?data=&msg=' + msg + '&type='
        if type != None:
            API_URL += str(type)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')
