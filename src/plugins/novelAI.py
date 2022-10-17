from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random
import requests
import os, base64
import platform
import json

catch_str = on_keyword({'/novel '})

plat = platform.system().lower()
if plat == 'windows':
    # 此处替换你的go-cqhttp路径
    gocqhttp_path = 'F:\\github_pro\\go-cqhttp'
elif plat == 'linux':
    gocqhttp_path = '/root/go-cqhttp'


@catch_str.handle()
async def send_img(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    # id = event.get_user_id()
    content = get_msg[7:]

    out = await get_img(content)
    out = "novel.png"
    msg = "[CQ:image,file=" + out + "]"
    await catch_str.finish(Message(f'{msg}'))


async def get_img(content):
    plat = platform.system().lower()

    if plat == 'windows':
        # print('windows系统')
        d = 'data\\'
        path = 'data\\novel.png'
        out = gocqhttp_path + '\\data\\images\\novel.png'
    elif plat == 'linux':
        # print('linux系统')
        d = 'data/'
        path = 'data/novel.png'
        out = gocqhttp_path + '/data/images/novel.png'

    # 判断目录是否存在，如果不存在建立目录
    if not os.path.exists(d):
        os.mkdir(d)

    # 如果此接口寄了，通过 https://api.smoe.me/v1/free 获取新接口替换
    API_URL = 'https://14553.gradio.app/api/predict'
    json1_str = '{"fn_index":13,"data":["' + content + '","","None","None",20,"Euler a",false,false,1,1,7,-1,-1,0,0,' \
                                                       '0,false,512,512,false,0.7,0,0,"None",false,false,null,"",' \
                                                       '"Seed","","Nothing","",true,false,false,null,"",""],' \
                                                       '"session_hash":"9d6qr6oftkh"} '
    json1 = json.loads(json1_str)
    ret = requests.post(API_URL, json=json1)
    ret = ret.json()
    # nonebot.logger.info(ret)

    img_str = ret["data"][0][0]
    img_str = img_str[22:]
    # nonebot.logger.info(img_str)

    img_data = base64.b64decode(img_str)  # 注意：如果是"data:image/jpg:base64,"，那你保存的就要以png格式，如果是"data:image/png:base64,"那你保存的时候就以jpg格式。
    with open(out, 'wb') as f:
        f.write(img_data)
        f.close()

    return out
