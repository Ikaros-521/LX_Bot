from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword, on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

catch_str = on_command("导航", aliases={"资源导航"}, block=True)


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    id = event.get_user_id()
    msg = "[CQ:at,qq={}]".format(id) + \
        '\nVTB数据看板：https://ikaros-521.gitee.io/vtb_data_board/' \
        '\nmatsuri：https://matsuri.icu/' \
        '\ndanmaku：https://danmaku.suki.club/' \
        '\nvtbs.fun：http://www.vtbs.fun/' \
        '\nbiligank：https://biligank.com/' \
        '\n火龙榜：https://huolonglive.com/#/' \
        '\nvtbs.moe：https://vtbs.moe/'

    await catch_str.finish(Message(f'{msg}'))
