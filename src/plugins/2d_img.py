import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random

catch_str = on_keyword({'/二次元1'})
@catch_str.handle()
async def send_img(bot: Bot, event: Event, state: T_State):
    msg = "[CQ:image,file=https://api.vvhan.com/api/acgimg?" + str(random.random()) + "]"
    await catch_str.finish(Message(f'{msg}'))


async def get_random_img():
    API_URL = 'https://shengapi.cn/api/bizi.php?msg=2?' + str(random.random())
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            ret = await response.read()
    ret = ret.decode('utf-8')
    # nonebot.logger.info(ret)
    url = ret[5:-1]
    return url


catch_str2 = on_keyword({'/二次元2'})
@catch_str2.handle()
async def send_img2(bot: Bot, event: Event, state: T_State):
    # get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    # id = event.get_user_id()
    msg = "[CQ:image,file=https://api.oick.cn/random/api.php?" + str(random.random()) + "]"
    await catch_str2.finish(Message(f'{msg}'))


catch_str3 = on_keyword({'/二次元3'})
@catch_str3.handle()
async def send_img3(bot: Bot, event: Event, state: T_State):
    # get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    # id = event.get_user_id()
    msg = "[CQ:image,file=https://iw233.cn/API/Random.php?" + str(random.random()) + "]"
    await catch_str3.finish(Message(f'{msg}'))
