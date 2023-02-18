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
/绕口令

生成一个绕口令

""".strip()

__plugin_meta__ = PluginMetadata(
    name = '绕口令生成器',
    description = '适用于nonebot2 v11的绕口令生成器',
    usage = help_text
)


# 所有的命令都在这哦，要改命令触发关键词的请自便
catch_str = on_command("绕口令")

# 
@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    try:
        data_json = await get_data()

        if data_json['code'] != 1:
            msg = '\n接口返回失败，可以重试，还不行就寄了'
            await catch_str.finish(Message(f'{msg}'), at_sender=True)

        msg = '\n标题：' + data_json['data']['title'] + '\n内容：' + data_json['data']['Msg']
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data():
    try:
        API_URL = 'http://ovooa.com/API/rao/api.php'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                result = await response.read()
                ret = json.loads(result)
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret
