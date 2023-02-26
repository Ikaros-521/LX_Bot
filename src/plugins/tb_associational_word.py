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
/淘宝联想词 传入商品名关键词
/百度联想词 传入关键词

返回淘宝/百度关于这个商品或其他相关的关键词  

""".strip()

__plugin_meta__ = PluginMetadata(
    name = '淘宝/百度联想词',
    description = '适用于nonebot2 v11的淘宝/百度联想词查询工具',
    usage = help_text
)


# 所有的命令都在这哦，要改命令触发关键词的请自便
catch_str = on_command("淘宝联想词")
catch_str2 = on_command("百度联想词")

# 
@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        data_json = await get_tb_data(content)
        msg = json.dumps(data_json, indent=2, ensure_ascii=False)
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


@catch_str2.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        data_json = await get_bd_data(content)
        msg = json.dumps(data_json, indent=2, ensure_ascii=False)
        await catch_str2.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str2.finish(Message(f'{msg}'), at_sender=True)


async def get_tb_data(content):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/taobaoword.php?msg=' + content
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                result = await response.read()
                ret = json.loads(result)
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret


async def get_bd_data(content):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/wl/baiduword.php?msg=' + content
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                result = await response.read()
                ret = json.loads(result)
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret