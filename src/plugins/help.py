from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_keyword({'/help'})

@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    id = event.get_user_id()
    msg = "[CQ:at,qq={}]".format(id) + '\n目前支持命令为：\n发表情 随机返回一个表情\n/翻译 输入命令后追加需要翻译的句子\n/求签 注意有空格分隔，求签内容追加在后方\n/二次元1 ' \
                                       '随机返回一张二次元图片\n/二次元2 随机返回一张二次元图片\n/二次元3 随机返回一张二次元图片\n/短链 ' \
                                       '注意有空格分隔，需要转换的链接追加在后方，且需要http头\n/端口扫描 注意有空格分隔，后面内容为：ip=域名 port=22,80,443等,' \
                                       '分隔追加\n/ping 注意有空格分隔，后面内容追加域名\n/查b 注意有空格分隔，后面内容追加b站用户uid，进行用户信息查询\n' \
                                       '直接复制直播链接（注意房间号后是空的），进行用户信息查询'
    await catch_str.finish(Message(f'{msg}'))
