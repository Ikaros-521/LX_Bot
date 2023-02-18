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
/兽语 你好
/兽语翻译 啊呜呜～呜嗷嗷～啊呜呜呜嗷～嗷嗷啊～啊呜呜啊嗷

""".strip()

__plugin_meta__ = PluginMetadata(
    name = '兽语生成器',
    description = '适用于nonebot2 v11的兽语生成器',
    usage = help_text
)


# 所有的命令都在这哦，要改命令触发关键词的请自便
catch_str = on_command("兽语", aliases={"兽语生成", "兽语加密"})
catch_str2 = on_command('兽语翻译', aliases={"兽语解密"})


# 
@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    try:
        data_json = await get_sho_u(content)

        if data_json['code'] != 1:
            msg = '\n接口返回失败，可以重试，还不行就寄了'
            await catch_str.finish(Message(f'{msg}'), at_sender=True)

        msg = data_json['data']['Message']
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


# 
@catch_str2.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    try:
        data_json = await get_sho_u(content, 1)

        if data_json['code'] != 1:
            msg = '\n接口返回失败，可以重试，还不行就寄了'
            await catch_str.finish(Message(f'{msg}'), at_sender=True)

        msg = data_json['data']['Message']
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_sho_u(msg, format=0):
    try:
        API_URL = 'http://ovooa.com/API/sho_u/?msg=' + msg + '&format=' + str(format)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                result = await response.read()
                ret = json.loads(result)
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret
