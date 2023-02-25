import aiohttp
from nonebot.adapters.onebot.v11 import Message
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_command('舔狗日记')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event):
    try:
        data = await get_data()
        msg = "\n" + data
    except:
        msg = "\n请求失败，可能是网络问题或者是API寄了~"

    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data():
    API_URL = 'https://www.xzccc.com/api/dog/'
    header1 = {
        'content-type': 'text/plain; charset=utf-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
    }
    async with aiohttp.ClientSession(headers=header1) as session:
        async with session.get(url=API_URL, headers=header1) as response:
            ret = await response.read()
    # nonebot.logger.info(ret)
    return ret.decode('utf-8')
