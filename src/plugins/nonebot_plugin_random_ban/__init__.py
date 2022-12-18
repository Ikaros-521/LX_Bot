from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
import nonebot
import random

# 命令权限 bot超管 群管理 群主
catch_str = on_command('随机禁言', aliases={"随禁"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@catch_str.handle()
async def send_msg(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    # nonebot.logger.info(content)
    # 最大禁言时间
    max_ban_time = random.randint(1, 60)
    try:
        if len(content) > 0:
            max_ban_time = random.randint(1, int(content))
    except:
        msg = "\n参数解析失败（请传入正整数的最大禁言时间）"
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    # 获取群号 event.group_id
    member_list = await bot.get_group_member_list(group_id=event.group_id)
    # nonebot.logger.info(member_list)
    # for member in member_list:
    #     nickname = member['card'] or member['nickname']
    #     user_id = member['user_id']
    #     nonebot.logger.info("nickname:" + nickname + " user_id=" + str(user_id))

    random_num = random.randint(0, len(member_list) - 1)
    # nonebot.logger.info("random_num:" + str(random_num))
    user_id = member_list[random_num]['user_id']
    nickname = member_list[random_num]['card'] or member_list[random_num]['nickname']
    # nonebot.logger.info("nickname:" + nickname + " user_id=" + str(user_id) + " time=" + str(max_ban_time))
    try:
        await bot.set_group_ban(group_id=event.group_id, user_id=user_id, duration=60 * max_ban_time)
    except:
        msg = "\n禁言失败~机器人权限不足（请确认bot是否是管理员/禁言到群管）"
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    msg = "\n恭喜幸运儿:" + nickname + " 获得" + str(max_ban_time) + "分钟的禁言服务"
    await catch_str.finish(Message(f'{msg}'), at_sender=True)
