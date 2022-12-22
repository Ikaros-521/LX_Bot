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

开启至暗时刻
命令结构：```/开启至暗时刻``` 或 ```/至暗时刻启动``` 或 ```/至暗时刻开启```  或 ```/启动至暗时刻```  
例如：```/开启至暗时刻```  

关闭至暗时刻
命令结构：```/关闭至暗时刻``` 或 ```/至暗时刻关闭``` 或 ```/停止至暗时刻```  或 ```/至暗时刻停止```  
例如：```/关闭至暗时刻```  
""".strip()

__plugin_meta__ = PluginMetadata(
    name = '随机禁言',
    description = '随机禁言一名群员或自己n分钟（n通过传入数字然后随机实现）',
    usage = help_text
)


# 任何人都可以使用 随机禁言
anyone_can_random_ban = []


# 获取env配置，不写入配置的话，每次重启都会重置为 至暗时刻关闭 的状态
try:
    nonebot.logger.debug(nonebot.get_driver().config.anyone_can_random_ban)
    anyone_can_random_ban = nonebot.get_driver().config.anyone_can_random_ban
except:
    nonebot.logger.warning("random_ban的anyone_can_random_ban没有配置，默认只有bot的超管、群管理和群主可以使用 随机禁言 功能。")

catch_str = on_command('随机禁言', aliases={"随禁"})


@catch_str.handle()
async def send_msg(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    # nonebot.logger.info(content)

    group_id = event.group_id

    nonebot.logger.debug(anyone_can_random_ban)

    # 判断是否 群管或拥有者(此为普通用户)
    if event.sender.role not in ["admin", "owner"] or "私聊" in msg:
        # 如果存在此群配置
        if group_id in anyone_can_random_ban:
            # 最大禁言时间
            max_ban_time = random.randint(1, 60)
            try:
                if len(content) > 0:
                    max_ban_time = random.randint(1, int(content))
            except:
                msg = "\n参数解析失败（请传入正整数的最大禁言时间）"
                await catch_str.finish(Message(f'{msg}'), at_sender=True)
            # 获取群号 event.group_id
            member_list = await bot.get_group_member_list(group_id=group_id)

            random_num = random.randint(0, len(member_list) - 1)
            # nonebot.logger.info("random_num:" + str(random_num))
            user_id = member_list[random_num]['user_id']
            nickname = member_list[random_num]['card'] or member_list[random_num]['nickname']
            # nonebot.logger.info("nickname:" + nickname + " user_id=" + str(user_id) + " time=" + str(max_ban_time))
            try:
                await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=60 * max_ban_time)
            except:
                msg = "\n禁言失败~机器人权限不足（请确认bot是否是管理员/禁言到群管）"
                await catch_str.finish(Message(f'{msg}'), at_sender=True)

            msg = "\n恭喜幸运儿:" + nickname + " 获得" + str(max_ban_time) + "分钟的禁言服务"
            await catch_str.finish(Message(f'{msg}'), at_sender=True)
        else:
            msg = '\n本群的至暗时刻还没开启，请告知群管发送"/至暗时刻开启"，启用功能'
            await catch_str.finish(Message(f'{msg}'), at_sender=True)
    # 是群管的话 随便用
    else:
        # 最大禁言时间
        max_ban_time = random.randint(1, 60)
        try:
            if len(content) > 0:
                max_ban_time = random.randint(1, int(content))
        except:
            msg = "\n参数解析失败（请传入正整数的最大禁言时间）"
            await catch_str.finish(Message(f'{msg}'), at_sender=True)
        # 获取群号 event.group_id
        member_list = await bot.get_group_member_list(group_id=group_id)

        random_num = random.randint(0, len(member_list) - 1)
        # nonebot.logger.info("random_num:" + str(random_num))
        user_id = member_list[random_num]['user_id']
        nickname = member_list[random_num]['card'] or member_list[random_num]['nickname']
        # nonebot.logger.info("nickname:" + nickname + " user_id=" + str(user_id) + " time=" + str(max_ban_time))
        try:
            await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=60 * max_ban_time)
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


catch_str3 = on_command('至暗时刻启动', aliases={"开启至暗时刻", "至暗时刻开启", "启动至暗时刻"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@catch_str3.handle()
async def send_msg(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    global anyone_can_random_ban

    group_id = event.group_id

    nonebot.logger.debug(anyone_can_random_ban)

    # 如果存在此群配置
    if group_id in anyone_can_random_ban:
        msg = "\n本群已开启 至暗时刻，无需重复启动。"
        await catch_str3.finish(Message(f'{msg}'), at_sender=True)
    else:
        anyone_can_random_ban.append(group_id)
        msg = "\n本群开启 至暗时刻成功，开始狩猎吧！"
        await catch_str3.finish(Message(f'{msg}'), at_sender=True)


catch_str4 = on_command('至暗时刻关闭', aliases={"关闭至暗时刻", "停止至暗时刻", "至暗时刻停止"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@catch_str4.handle()
async def send_msg(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    global anyone_can_random_ban

    group_id = event.group_id

    nonebot.logger.debug(anyone_can_random_ban)

    # 如果存在此群配置
    if group_id in anyone_can_random_ban:
        anyone_can_random_ban.remove(group_id)
        msg = "\n本群已关闭 至暗时刻，世界恢复和平。"
        await catch_str4.finish(Message(f'{msg}'), at_sender=True)
    else:
        msg = "\n本群未开启 至暗时刻，无需关闭。"
        await catch_str4.finish(Message(f'{msg}'), at_sender=True)

