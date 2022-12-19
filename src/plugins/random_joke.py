import aiohttp, json
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg


catch_str = on_command('笑话')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    data_json = await get_data()
    try:
        msg = '\n' + data_json["result"][0]["content"]
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data():
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/95
    api_key = ""
    API_URL = 'http://v.juhe.cn/joke/randJoke.php?key=' + api_key
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret
