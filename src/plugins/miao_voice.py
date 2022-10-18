from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import requests
import random
import os
import platform

# 注意发送语音依赖ffmpeg，并配置到环境变量.
# 特别提示：linux安装ffmpeg后配置path，如果还不行 则给ffmpeg添加软链（例：ln -s /usr/local/ffmpeg/bin/ffmpeg /usr/local/bin/ffmpeg）
catch_str = on_keyword({'/喵一个 '})

# 数组中存放你想要快速匹配的昵称, paths存放 go-cqhttp\data\voices\下的文件路径
names = ['笨笨']
plat = platform.system().lower()
if plat == 'windows':
    # print('windows系统')
    gocqhttp_path = 'E:\\GitHub_pro\\go-cqhttp\\data\\voices\\'
    paths = ['miao\\benben\\']
elif plat == 'linux':
    # print('linux系统')
    gocqhttp_path = '/root/go-cqhttp/data/voices/'
    paths = ['miao/benben/']

@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[5:]

    for i, name in enumerate(names):
        if name == content:
            voice_len = len(os.listdir(gocqhttp_path + paths[i]))
            nonebot.logger.info("voice_len=" + str(voice_len))
            random_num = random.randint(17, voice_len)
            nonebot.logger.info("random_num=" + str(random_num))

            file_path = paths[i] + str(random_num) + ".mp3"
            # nonebot.logger.info(file_path)
            msg = "[CQ:record,file=" + file_path + "]"

            await catch_str.finish(Message(f'{msg}'))

