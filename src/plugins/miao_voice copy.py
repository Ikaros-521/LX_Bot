from nonebot.adapters.onebot.v11 import Message
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random
import os
import platform

catch_str = on_command('喵一个')

# 数组中存放你想要快速匹配的昵称
names = ['笨笨', '火羽']
plat = platform.system().lower()
if plat == 'windows':
    # print('windows系统')
    gocqhttp_path = 'E:\GitHub_pro\go-cqhttp\data\\voices\\'
    paths = ['miao\\benben\\', 'miao\\hinome\\']
elif plat == 'linux':
    # print('linux系统')
    gocqhttp_path = '/root/go-cqhttp/data/voices/'
    paths = ['miao/benben/', 'miao/hinome/']

@catch_str.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    # 以空格分割 昵称 文件名（设定为1开始的递增数字）
    content = content.split()
    have_filename = 1
    try:
        filename_in = content[1]
        # nonebot.logger.info(filename_in)
    except (KeyError, TypeError, IndexError) as e:
        have_filename = 0

    for i, name in enumerate(names):
        if name == content[0]:
            voice_len = len(os.listdir(gocqhttp_path + paths[i]))
            nonebot.logger.info("voice_len=" + str(voice_len))
            if have_filename == 0:
                random_num = random.randint(1, voice_len)
            else:
                random_num = int(filename_in)
            nonebot.logger.info("random_num=" + str(random_num))

            msg = "[CQ:record,file=" + paths[i] + str(random_num) + ".mp3]"
            await catch_str.finish(Message(f'{msg}'))
