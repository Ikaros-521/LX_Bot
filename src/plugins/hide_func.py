from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_keyword({'/隐藏功能'})

@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    id = event.get_user_id()
    msg = "[CQ:at,qq={}]".format(id) + '\n目前支持的简单命令为（直接发送命令即可，例:/猫猫）：\n' \
                                       '【/cos1】 随机返回一张cos图片\n' \
                                       '【/cos2】 随机返回一张小姐姐图片\n' \
                                       '【/查火羽】 懂的都懂\n' \
                                       '\n目前支持的高级命令为（发送内容为命令 空格 解析文本，例:/搜图 机器人）：\n' \
                                       '【/搜图 】 搜索内容追加在后方（百度图库）\n ' \
                                       '【/搜图WH 】 搜索内容追加在后方（wallhaven图库，不支持中文）\n' \
                                       '【/搜图WH2 】 搜索内容追加在后方（wallhaven图库原图，不支持中文）\n' \
                                       '【/r18 】 追加搜索标签和r18开启标识符，例：（/r18 学生 0)\n '
    await catch_str.finish(Message(f'{msg}'))
