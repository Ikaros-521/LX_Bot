import nonebot
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.params import CommandArg
import aiohttp, json


from nonebot.plugin import PluginMetadata


help_text = f"""
插件命令：
/温柔语录
/微甜语录
/超强语录 传入语录id（不传id可以获取id列表）

生成语录

""".strip()

__plugin_meta__ = PluginMetadata(
    name = '小白API语录生成器',
    description = '适用于nonebot2 v11的小白API语录生成器',
    usage = help_text
)


# 所有的命令都在这哦，要改命令触发关键词的请自便
catch_str = on_command("温柔语录")
catch_str2 = on_command("微甜语录")
catch_str3 = on_command("超强语录")

# 
@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    try:
        msg = await get_quotation(0)

        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


@catch_str2.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    try:
        msg = await get_quotation(1)

        await catch_str2.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str2.finish(Message(f'{msg}'), at_sender=True)


@catch_str3.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    content = content.split()

    id = 1

    try:
        if len(content) == 0:
            msg = '\n语录id：\n' + await get_super_quotation(0)
            await catch_str3.finish(Message(f'{msg}'), at_sender=True)
        else:
            id = int(content[0])

            msg = await get_super_quotation(id)
            await catch_str3.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str3.finish(Message(f'{msg}'), at_sender=True)


async def get_quotation(type):
    try:
        if type == 0:
            API_URL = 'http://ovooa.com/API/wryl/api.php'
        elif type == 1:
            API_URL = 'https://xiaobai.klizi.cn/API/other/wtqh.php'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')


async def get_super_quotation(id):
    try:
        if id == 0:
            API_URL = 'https://xiaobai.klizi.cn/API/other/cqyl.php?data=&id='
        else:
            API_URL = 'https://xiaobai.klizi.cn/API/other/cqyl.php?data=&id=' + str(id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')