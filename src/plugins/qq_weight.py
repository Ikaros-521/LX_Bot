import aiohttp, json
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg


catch_str = on_command('权重')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    data_json = await get_data(content)

    msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)

    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data(content):
    API_URL = 'http://tfapi.top/API/qqqz.php?type=json&qq=' + content
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret
