import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot

catch_str = on_keyword({'/线稿'})


@catch_str.handle()
async def send_msg(bot: Bot, event: MessageEvent, state: T_State):
    id = event.get_user_id()

    if isinstance(event, MessageEvent):
        for msg in event.message:
            if msg.type == "image":
                url: str = msg.data["url"]
                # state["url"] = url
                # nonebot.logger.info('url:' + url)
                data = await get_data(url)
                msg = "[CQ:image,file=" + data + "]"
                await catch_str.finish(Message(f'{msg}'))
                return

        msg = "[CQ:at,qq={}]".format(id) + '\n请传入图片喵'
        await catch_str.finish(Message(f'{msg}'))
        return


async def get_data(url):
    API_URL = 'https://shengapi.cn/api/Line_Draft/?url=' + url
    header1 = {
        'content-type': 'text/plain; charset=utf-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
    }
    async with aiohttp.ClientSession(headers=header1) as session:
        async with session.get(url=API_URL, headers=header1) as response:
            ret = await response.read()
    # nonebot.logger.info(ret)
    return ret.decode('utf-8')
