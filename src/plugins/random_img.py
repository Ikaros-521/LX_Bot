import json

import aiohttp
from nonebot.adapters.onebot.v11 import Message
from nonebot import on_command, on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random

catch_str = on_command('猫猫')
catch_str2 = on_command('狗狗')
catch_str3 = on_keyword({'发表情'})


@catch_str.handle()
async def _(bot: Bot, event: Event):
    url = await get_random_img()
    msg = "[CQ:image,file=" + url + "]"
    nonebot.logger.info(msg)
    await catch_str.finish(Message(f'{msg}'))


async def get_random_img():
    API_URL = 'https://api.thecatapi.com/v1/images/search?limit=1&size=full&breed_id=amis&' + str(random.random())
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            json1 = json.loads(result)
    # nonebot.logger.info(json1)
    url = json1[0]["url"]
    return url


@catch_str2.handle()
async def _(bot: Bot, event: Event):
    url = await get_random_img2()
    msg = "[CQ:image,file=" + url + "]"
    await catch_str2.finish(Message(f'{msg}'))


async def get_random_img2():
    API_URL = 'https://dog.ceo/api/breeds/image/random?' + str(random.random())
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            json1 = json.loads(result)
    # nonebot.logger.info(json)
    url = json1["message"].replace('\\', '')
    return url


@catch_str3.handle()
async def _(bot: Bot, event: Event):

    emoji_msg = "[CQ:face,id=" + str(random.randint(0, 221)) + "]"
    await catch_str3.send(Message(emoji_msg))
