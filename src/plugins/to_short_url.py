import aiohttp
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import nonebot

catch_str = on_keyword({'/短链 '})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    src = get_msg[4:]
    url = await get_short_url(src)

    id = event.get_user_id()
    msg = "[CQ:at,qq={}]".format(id) + '\n短链为：' + url
    await catch_str.finish(Message(f'{msg}'))


async def get_short_url(src):
    apiKey = '8e35524a0115468f2f08a8ba253362f1'
    API_URL = 'https://shengapi.cn/api/dwz.php?url=' + src + '&apiKey=' + apiKey
    header1 = {
        'content-type': 'text/plain; charset=utf-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
    }
    async with aiohttp.ClientSession(headers=header1) as session:
        async with session.get(url=API_URL, headers=header1) as response:
            ret = await response.read()
    # nonebot.logger.info(ret)
    return ret.decode('utf-8')
