import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random

catch_str = on_keyword({'/二次元1'})
@catch_str.handle()
async def _(bot: Bot, event: Event, state: T_State):
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
async def _(bot: Bot, event: Event):
    # get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    # id = event.get_user_id()
    msg = "[CQ:image,file=https://api.oick.cn/random/api.php?" + str(random.random()) + "]"
    await catch_str2.finish(Message(f'{msg}'))


catch_str3 = on_keyword({'/二次元3'})
@catch_str3.handle()
async def _(bot: Bot, event: Event):
    # get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    # id = event.get_user_id()
    msg = "[CQ:image,file=https://iw233.cn/API/Random.php?" + str(random.random()) + "]"
    await catch_str3.finish(Message(f'{msg}'))


catch_str4 = on_keyword({'/二次元4'})
@catch_str4.handle()
async def _(bot: Bot, event: Event):
    msg = "http://nya.nikiss.top/img_api?fw=1&mode=%E4%BA%8C%E6%AC%A1%E5%85%83"
    await catch_str4.finish(Message(f'{msg}'))


catch_str5 = on_keyword({'/cos1'})


@catch_str5.handle()
async def _(bot: Bot, event: Event, state: T_State):
    # get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    # id = event.get_user_id()
    msg = "[CQ:image,file=https://api.vvhan.com/api/girl?" + str(random.random()) + "]"

    await catch_str5.finish(Message(f'{msg}'))
    # await catch_str.finish(Message(MessageSegment.image('https://api.vvhan.com/api/girl?2')))


catch_str6 = on_keyword({'/cos2'})


@catch_str6.handle()
async def _(bot: Bot, event: Event, state: T_State):
    # get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    # id = event.get_user_id()
    msg = "[CQ:image,file=https://api.linhun.vip/api/Littlesister?" + str(random.random()) + "]"

    await catch_str6.finish(Message(f'{msg}'))
    # await catch_str.finish(Message(MessageSegment.image('https://api.vvhan.com/api/girl?2')))


catch_str7 = on_keyword({'/cos3'})


@catch_str7.handle()
async def _(bot: Bot, event: Event, state: T_State):
    msg = "http://nya.nikiss.top/img_api?fw=1&mode=%E4%B8%89%E6%AC%A1%E5%85%83"

    await catch_str7.finish(Message(f'{msg}'))


catch_str8 = on_keyword({'/二次元5'})

@catch_str8.handle()
async def _(bot: Bot, event: Event, state: T_State):
    with open('data/tutu_local_img_lib/2d.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        random_line = random.choice(lines)

    msg = "[CQ:image,file=" + random_line[:-1] + "]"

    await catch_str8.finish(Message(f'{msg}'))


catch_str9 = on_keyword({'/cos4'})

@catch_str9.handle()
async def _(bot: Bot, event: Event, state: T_State):
    with open('data/tutu_local_img_lib/3d.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        random_line = random.choice(lines)

    msg = "[CQ:image,file=" + random_line[:-1] + "]"

    await catch_str9.finish(Message(f'{msg}'))
