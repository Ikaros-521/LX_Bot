import aiohttp
from nonebot.adapters.onebot.v11 import Message
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_command('历史上今天')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event):
    data = await get_data()
    msg = '\n' + data

    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data():
    # 替换自己的api key
    apiKey = '904388f1cf61032e6cb0133653715524'
    API_URL = 'https://api.linhun.vip/api/history?format=json&apiKey=' + apiKey

    header1 = {
        'content-type': 'text/plain; charset=utf-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
    }
    async with aiohttp.ClientSession(headers=header1) as session:
        async with session.get(url=API_URL, headers=header1) as response:
            ret = await response.read()
    # nonebot.logger.info(ret)
    return ret.decode('utf-8')
