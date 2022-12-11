# import datetime
import json

import nonebot
# import requests
# import asyncio
import aiohttp
# import time
# from io import BytesIO
from nonebot import on_keyword, on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.typing import T_State
# from nonebot_plugin_imageutils import Text2Image
from nonebot_plugin_htmlrender import (
    text_to_pic,
    md_to_pic,
    template_to_pic,
    get_new_page,
)


catch_str = on_command("配色方案", aliases={"配色"})


@catch_str.handle()
async def _(bot: Bot, event: Event, state: T_State):
    json_data = await get_colormind()

    color_codes = []
    msg = ""

    try:
        msg += "推荐的配色方案为："
        for color in json_data["result"]:
            r, g, b = color
            color_code = "#{:02X}{:02X}{:02X}".format(r, g, b)
            color_codes.append(color_code)
            msg += color_code + " "
    except:
        msg = '\n调用接口失败，寄！'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
        return

    img_str = ""
    for color_code in color_codes:
        img_str += '<font color="' + color_code + '" size=7>█</font>'

    output = await md_to_pic(md=img_str, width=230)

    await catch_str.finish(Message(MessageSegment.text(msg) + MessageSegment.image(output)), at_sender=True)


async def get_colormind():
    header1 = {
        'content-type': 'text/plain; charset=utf-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
    }
    API_URL = 'http://colormind.io/api/'
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=API_URL, 
            headers=header1,
            json={"model": "default"}
        ) as response:
            result = await response.read()
            # nonebot.logger.info(result)
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret