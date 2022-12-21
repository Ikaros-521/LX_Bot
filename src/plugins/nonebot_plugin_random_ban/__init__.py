from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
import nonebot
import random
from nonebot.plugin import PluginMetadata


help_text = f"""
随机禁言一名群员
命令结构：/随机禁言 [最大禁言时间] 或 /随禁 [最大禁言时间] （最大禁言时间不填默认60分钟内的随机）  
例如：/随机禁言 或 /随禁 10  

随机禁言自己
命令结构：/口球 [最大禁言时间] 或 /禁我 [最大禁言时间] （最大禁言时间不填默认60分钟内的随机）  
例如：/口球 或 /禁我 10  
""".strip()

__plugin_meta__ = PluginMetadata(
    name = '随机禁言',
    description = '随机禁言一名群员或自己n分钟（n通过传入数字然后随机实现）',
    usage = help_text
)


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


catch_str2 = on_command('口球', aliases={"禁我"})


@catch_str2.handle()
async def send_msg(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    user_id = event.get_user_id()
    content = msg.extract_plain_text()
    # nonebot.logger.info(content)
    # 最大禁言时间
    max_ban_time = random.randint(1, 60)
    try:
        if len(content) > 0:
            max_ban_time = random.randint(1, int(content))
    except:
        msg = "\n参数解析失败（请传入正整数的最大禁言时间）"
        await catch_str2.finish(Message(f'{msg}'), at_sender=True)
    # 获取群号 event.group_id
    # member_list = await bot.get_group_member_list(group_id=event.group_id)

    # nonebot.logger.info("random_num:" + str(random_num))
    # nickname = member_list[random_num]['card'] or member_list[random_num]['nickname']
    # nonebot.logger.info("nickname:" + nickname + " user_id=" + str(user_id) + " time=" + str(max_ban_time))
    try:
        await bot.set_group_ban(group_id=event.group_id, user_id=user_id, duration=60 * max_ban_time)
    except:
        msg = "\n禁言失败~机器人权限不足（请确认bot是否是管理员/禁言到群管）"
        await catch_str2.finish(Message(f'{msg}'), at_sender=True)

    msg = "\n恭喜您获得" + str(max_ban_time) + "分钟的禁言服务"
    await catch_str2.finish(Message(f'{msg}'), at_sender=True)
