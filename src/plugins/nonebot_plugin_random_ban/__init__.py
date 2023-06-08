from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
import nonebot
import random, re
from nonebot.plugin import PluginMetadata
from nonebot.exception import FinishedException


help_text = f"""
随机禁言一名群员
命令结构：/随机禁言 [最大禁言时间] 或 /随禁 [最大禁言时间] （最大禁言时间不填默认60分钟内的随机）  
例如：/随机禁言 或 /随禁 10 或 /随禁 10分 或 /随禁 10时 或 /随禁 10天 

随机禁言自己
命令结构：/口球 [最大禁言时间] 或 /禁我 [最大禁言时间] （最大禁言时间不填默认60分钟内的随机）  
例如：/口球 或 /禁我 10 或 /禁我 10分 或 /口球 10时 或 /口球 10天 

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


# 正则匹配时间
def parse_time_string(time_string):
    pattern = r'(\d+(?:\.\d+)?)(?:分钟|分|小时|时|天)?'
    match = re.match(pattern, time_string)

    # print(f"time_string={time_string}")

    if match:
        groups = match.groups()
        num_groups = len(groups)

        if num_groups == 1:
            value = float(groups[0])
            return int(value)  # 纯数字情况

        value = float(match.group(1))
        unit = match.group(2)

        if unit == '分钟' or unit == '分':
            return int(value)
        elif unit == '小时' or unit == '时':
            return int(value * 60)
        elif unit == '天':
            return int(value * 60 * 24)

        # 纯数字情况
        return int(value)

    return None


# 分钟数转换为 "x天x小时x分钟"
def format_minutes(minutes):
    days = minutes // (60 * 24)
    hours = (minutes % (60 * 24)) // 60
    remaining_minutes = minutes % 60

    result = ""
    if days > 0:
        result += str(days) + "天"
    if hours > 0:
        result += str(hours) + "小时"
    if remaining_minutes > 0:
        result += str(remaining_minutes) + "分钟"

    return result



@catch_str.handle()
async def send_msg(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
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
                    tmp = parse_time_string(content)
                    if tmp is None:
                        msg = "参数解析失败（请传入正整数的最大禁言时间）"
                        await catch_str.finish(Message(f'{msg}'), reply_message=True)
                    max_ban_time = random.randint(1, tmp)
            except FinishedException:
                pass
            except Exception as e:
                print(e)
                msg = "参数解析失败（请传入正整数的最大禁言时间）"
                await catch_str.finish(Message(f'{msg}'), reply_message=True)
            # 获取群号 event.group_id
            member_list = await bot.get_group_member_list(group_id=group_id)

            random_num = random.randint(0, len(member_list) - 1)
            # nonebot.logger.info("random_num:" + str(random_num))
            user_id = member_list[random_num]['user_id']
            nickname = member_list[random_num]['card'] or member_list[random_num]['nickname']
            # nonebot.logger.info("nickname:" + nickname + " user_id=" + str(user_id) + " time=" + str(max_ban_time))
            try:
                await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=60 * max_ban_time)
            except FinishedException:
                pass
            except Exception as e:
                print(e)
                msg = "禁言失败~机器人权限不足（请确认bot是否是管理员/禁言到群管）"
                await catch_str.finish(Message(f'{msg}'), reply_message=True)

            msg = "恭喜幸运儿:" + nickname + " 获得" + format_minutes(max_ban_time) + "的禁言服务"
            await catch_str.finish(Message(f'{msg}'), reply_message=True)
        else:
            msg = '本群的至暗时刻还没开启，请告知群管发送"/至暗时刻开启"，启用功能'
            await catch_str.finish(Message(f'{msg}'), reply_message=True)
    # 是群管的话 随便用
    else:
        # 最大禁言时间
        max_ban_time = random.randint(1, 60)
        try:
            if len(content) > 0:
                tmp = parse_time_string(content)
                # print(f"tmp={tmp}")
                if tmp is None:
                    msg = "参数解析失败（请传入正整数的最大禁言时间）"
                    await catch_str.finish(Message(f'{msg}'), reply_message=True)
                max_ban_time = random.randint(1, tmp)
        except FinishedException:
            pass
        except Exception as e:
            print(e)
            msg = "参数解析失败（请传入正整数的最大禁言时间）"
            await catch_str.finish(Message(f'{msg}'), reply_message=True)
        # 获取群号 event.group_id
        member_list = await bot.get_group_member_list(group_id=group_id)

        random_num = random.randint(0, len(member_list) - 1)
        # nonebot.logger.info("random_num:" + str(random_num))
        user_id = member_list[random_num]['user_id']
        nickname = member_list[random_num]['card'] or member_list[random_num]['nickname']
        # nonebot.logger.info("nickname:" + nickname + " user_id=" + str(user_id) + " time=" + str(max_ban_time))
        try:
            await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=60 * max_ban_time)
        except FinishedException:
            pass
        except Exception as e:
            print(e)
            msg = "禁言失败~机器人权限不足（请确认bot是否是管理员/禁言到群管）"
            await catch_str.finish(Message(f'{msg}'), reply_message=True)

        msg = "恭喜幸运儿:" + nickname + " 获得" + format_minutes(max_ban_time) + "的禁言服务"
        await catch_str.finish(Message(f'{msg}'), reply_message=True)


catch_str2 = on_command('口球', aliases={"禁我"})


@catch_str2.handle()
async def send_msg(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    user_id = event.get_user_id()
    content = msg.extract_plain_text().strip()
    # nonebot.logger.info(content)
    # 最大禁言时间
    max_ban_time = random.randint(1, 60)
    try:
        if len(content) > 0:
            tmp = parse_time_string(content)
            if tmp is None:
                msg = "参数解析失败（请传入正整数的最大禁言时间）"
                await catch_str.finish(Message(f'{msg}'), reply_message=True)
            max_ban_time = random.randint(1, tmp)
    except FinishedException:
        pass
    except Exception as e:
        print(e)
        msg = "参数解析失败（请传入正整数的最大禁言时间）"
        await catch_str2.finish(Message(f'{msg}'), reply_message=True)
    # 获取群号 event.group_id
    # member_list = await bot.get_group_member_list(group_id=event.group_id)

    # nonebot.logger.info("random_num:" + str(random_num))
    # nickname = member_list[random_num]['card'] or member_list[random_num]['nickname']
    # nonebot.logger.info("nickname:" + nickname + " user_id=" + str(user_id) + " time=" + str(max_ban_time))
    try:
        await bot.set_group_ban(group_id=event.group_id, user_id=user_id, duration=60 * max_ban_time)
    except Exception as e:
        print(e)
        msg = "禁言失败~机器人权限不足（请确认bot是否是管理员/禁言到群管）"
        await catch_str2.finish(Message(f'{msg}'), reply_message=True)

    msg = "恭喜您获得" + format_minutes(max_ban_time) + "的禁言服务"
    await catch_str2.finish(Message(f'{msg}'), reply_message=True)


catch_str3 = on_command('至暗时刻启动', aliases={"开启至暗时刻", "至暗时刻开启", "启动至暗时刻"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@catch_str3.handle()
async def send_msg(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    global anyone_can_random_ban

    group_id = event.group_id

    nonebot.logger.debug(anyone_can_random_ban)

    # 如果存在此群配置
    if group_id in anyone_can_random_ban:
        msg = "本群已开启 至暗时刻，无需重复启动。"
        await catch_str3.finish(Message(f'{msg}'), reply_message=True)
    else:
        anyone_can_random_ban.append(group_id)
        msg = "本群开启 至暗时刻成功，开始狩猎吧！"
        await catch_str3.finish(Message(f'{msg}'), reply_message=True)


catch_str4 = on_command('至暗时刻关闭', aliases={"关闭至暗时刻", "停止至暗时刻", "至暗时刻停止"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@catch_str4.handle()
async def send_msg(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    global anyone_can_random_ban

    group_id = event.group_id

    nonebot.logger.debug(anyone_can_random_ban)

    # 如果存在此群配置
    if group_id in anyone_can_random_ban:
        anyone_can_random_ban.remove(group_id)
        msg = "本群已关闭 至暗时刻，世界恢复和平。"
        await catch_str4.finish(Message(f'{msg}'), reply_message=True)
    else:
        msg = "本群未开启 至暗时刻，无需关闭。"
        await catch_str4.finish(Message(f'{msg}'), reply_message=True)
