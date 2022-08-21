from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random
import requests

catch_str = on_keyword({'/猫猫'})


@catch_str.handle()
async def send_img(bot: Bot, event: Event, state: T_State):
    # get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    # id = event.get_user_id()
    url = await get_random_img()
    msg = "[CQ:image,file=" + url + "]"
    nonebot.logger.info(msg)
    await catch_str.finish(Message(f'{msg}'))


async def get_random_img():
    API_URL = 'https://api.thecatapi.com/v1/images/search?limit=1&size=full&breed_id=amis&' + str(random.random())
    ret = requests.get(API_URL)
    json = ret.json()
    # nonebot.logger.info(json)
    url = json[0]["url"]
    return url
