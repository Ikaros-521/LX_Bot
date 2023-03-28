import json
import asyncio
import aiohttp
import os
from pathlib import Path
import time, datetime
import traceback

import nonebot
# from nonebot import get_bot
from nonebot.log import logger
from nonebot import require, on_command
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
from nonebot.exception import FinishedException

require("nonebot_plugin_htmlrender")

from nonebot_plugin_htmlrender import (
    # md_to_pic,
    get_new_page,
)
from nonebot.plugin import PluginMetadata


help_text = f"""
命令列表：
发送命令查看：/开团帮助
""".strip()

__plugin_meta__ = PluginMetadata(
    name = '剑网三开团插件',
    description = '适用于nonebot2 v11的剑网三开团插件',
    usage = help_text
)


superuser = []
global_config = nonebot.get_driver().config

# 数据存储路径
root_dir = "data"
data_dir = root_dir + "/jx3_open_group"
data_path = ""

cmd0 = on_command("开团帮助")
cmd1 = on_command("开团", aliases={"创建团本", "创建团队", "开团本", "开团队"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
cmd2 = on_command("报名", aliases={"报名团本", "报名团队"})
cmd3 = on_command("取消报名", aliases={"取消最后报名"})
cmd10 = on_command("取消报名2", aliases={"取消最先报名"})
cmd4 = on_command("结束团本", aliases={"结束团队"})
cmd5 = on_command("团本列表", aliases={"团队列表"})
cmd6 = on_command("查团", aliases={"查询团本"})
cmd7 = on_command("开除团队", aliases={"开除团队倒序"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
cmd8 = on_command("清空团本", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
cmd9 = on_command("清空报名", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
cmd11 = on_command("开除团队2", aliases={"开除团队正序"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


# 开团帮助
@cmd0.handle()
async def _(bot: Bot, event: Event):
    cur_path = os.path.abspath(__file__)
    # 获取当前脚本所在目录的路径
    dir_path = os.path.dirname(cur_path)
    # print(dir_path)
    img_path = Path(dir_path + '/html/img/help.png')
    # print(img_path)
    await cmd0.finish(MessageSegment.image(img_path))


# 开团 <团名+时间>
@cmd1.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    qq = event.get_user_id()
    group_id = event.group_id

    data_path = await check_data_file(group_id)
    
    if content == "":
        msg = '命令错误，请传入团本描述，命令：/开团 <团本标题+时间>'
        await cmd1.finish(Message(f'{msg}'), reply_message=True)

    data_json = {}
    new_last_key = 0

    # 待插入文件的数据
    temp_json = {
        "标题": content,
        "副本最大人数": 25,
        "创始人QQ": qq,
        "创建时间": await get_current_datetime(),
        "用户列表": [
        ]
    }

    # await cmd1.send('开团中，请稍后...', reply_message=True)

    try:
        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)
        
            # 如果是空数据
            if len(data_json) == 0:
                last_key = 0
            else:
                # 获取最后一个键值对的键名
                last_key = list(data_json.keys())[-1]

                # 输出最后一个键名
                logger.debug("最后一个键名:" + last_key)

            new_last_key = str(int(last_key) + 1)

            # 向 data_json 中插入新的 JSON 数据
            data_json[new_last_key] = temp_json

            # 向 temp_json 中增加键值对
            temp_json["编号"] = new_last_key

        # 将处理后的JSON数据写入文件
        with open(data_path, 'w', encoding="utf-8") as f:
            json.dump(data_json, f, ensure_ascii=False)

        # 注释下行的话，可以返回开团图
        msg = '开团成功。团本编号：' + str(new_last_key)
        await cmd1.finish(msg, reply_message=True)

        dir_path = Path(__file__).parent
        file_path = dir_path / "html" / "index.html"

        async with get_new_page(viewport={"width": 1100, "height": 100}) as page:
            await page.goto(
                "file://" + str(file_path.resolve()),
                timeout=2 * 60 * 1000,
                wait_until="networkidle",
            )
            await page.eval_on_selector('html', "load_data('{}')".format(json.dumps(temp_json)))
            await asyncio.sleep(1)
            temp_path = "./data/jx3_open_group/index" + await get_current_timestamp_seconds() + ".png"
            pic = await page.screenshot(full_page=True, path=temp_path)

        await cmd1.finish(MessageSegment.image(pic))
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '创建团本失败！（请看后台日志排查问题）'
        await cmd1.finish(Message(f'{msg}'), reply_message=True)


# 报名 <团本编号> <门派> <id>
@cmd2.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    content = content.split()

    group_id = event.group_id

    data_path = await check_data_file(group_id)

    if len(content) != 3:
        msg = '命令错误，命令：/报名 <团本编号> <门派> <id>'
        await cmd2.finish(Message(f'{msg}'), reply_message=True)


    code = content[0]
    sect = content[1]
    id = content[2]
    qq = event.get_user_id()

    if len(id) > 7:
        msg = '命令错误，id超长，最长为7个字符。'
        await cmd2.finish(Message(f'{msg}'), reply_message=True)

    # 门派二维数组 内 外 肉 奶 （注意：这里改了，index.js也需要改）
    sect_arrs = [
        ["焚影", "花间游", "花间", "莫问", "毒经",
        "dj", "紫霞功", "气纯", "天罗诡道", "田螺",
        "无方", "冰心", "易筋经", "和尚", "太玄经",
        "衍天"],
        ["藏剑", "太虚剑意", "剑纯", "惊羽诀", "鲸鱼", 
        "傲雪战意", "天策", "北傲", "霸刀", "隐龙", 
        "凌雪", "笑尘", "丐帮", "凌海诀", "蓬莱", 
        "分山劲", "苍云", "孤锋诀", "刀宗"],
        ["铁骨", "铁王八", "铁牢律", "策T", "明尊琉璃体",
        "喵T", "洗髓", "和尚T"],
        ["相知", "奶歌", "灵素", "药奶", "补天",
        "奶毒", "离经易道", "奶花", "云裳心经", "奶秀"]
    ]

    data_json = {}

    # 待插入文件的数据
    temp_json = {
        "门派": sect, 
        "ID": id, 
        "QQ": qq
    }

    try:
        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)
        
            # 判断团本编号是否存在
            if code in data_json:             
                # 职业人数统计
                nei_num = 0
                wai_num = 0
                rou_num = 0
                nai_num = 0
                # 判断该职业是否已经满人了
                for users in data_json[code]["用户列表"]:
                    # 重复性检测
                    if users['ID'] == temp_json['ID']:
                        msg = '团本编号：' + code + "，已存在此ID用户，请勿重复报名！"
                        await cmd2.finish(Message(f'{msg}'), reply_message=True)

                    if users["门派"] in sect_arrs[0]:
                        nei_num += 1
                    elif users["门派"] in sect_arrs[1]:
                        wai_num += 1
                    elif users["门派"] in sect_arrs[2]:
                        rou_num += 1
                    elif users["门派"] in sect_arrs[3]:
                        nai_num += 1
                nei_wai_num = nei_num + wai_num
                rou_nai_num = rou_num + nai_num
                all_num =  nei_wai_num + rou_nai_num

                # logger.debug("nei_wai_num=" + str(nei_wai_num))
                # logger.debug("rou_nai_num=" + str(rou_nai_num))
                # logger.debug("all_num=" + str(all_num))

                 # 判断人数是否满了
                if all_num >= data_json[code]["副本最大人数"]:
                    msg = '团本编号：' + code + "，已满员，请勿继续报名！"
                    await cmd2.finish(Message(f'{msg}'), reply_message=True)

                # 内 外 肉 奶
                if sect in sect_arrs[0]:
                    if nei_num >= 13:
                        msg = '团本编号：' + code + "，内功已满员，报名失败！"
                        await cmd2.finish(Message(f'{msg}'), reply_message=True)
                    elif nei_num > 6:
                        if nei_wai_num >= 20:
                            msg = '团本编号：' + code + "，内功已满员，报名失败！"
                            await cmd2.finish(Message(f'{msg}'), reply_message=True)
                        elif nei_wai_num == 19:
                            if rou_nai_num >= 6:
                                msg = '团本编号：' + code + "，内功已满员，报名失败！"
                                await cmd2.finish(Message(f'{msg}'), reply_message=True)
                        elif nei_wai_num == 18:
                            if rou_nai_num >= 7:
                                msg = '团本编号：' + code + "，内功已满员，报名失败！"
                                await cmd2.finish(Message(f'{msg}'), reply_message=True)
                elif sect in sect_arrs[1]:
                    if wai_num >= 13:
                        msg = '团本编号：' + code + "，外功已满员，报名失败！"
                        await cmd2.finish(Message(f'{msg}'), reply_message=True)
                    if wai_num > 6:
                        if nei_wai_num >= 20:
                            msg = '团本编号：' + code + "，外功已满员，报名失败！"
                            await cmd2.finish(Message(f'{msg}'), reply_message=True)
                        elif nei_wai_num == 19:
                            if rou_nai_num >= 6:
                                msg = '团本编号：' + code + "，外功已满员，报名失败！"
                                await cmd2.finish(Message(f'{msg}'), reply_message=True)
                        elif nei_wai_num == 18:
                            if rou_nai_num >= 7:
                                msg = '团本编号：' + code + "，外功已满员，报名失败！"
                                await cmd2.finish(Message(f'{msg}'), reply_message=True)
                elif sect in sect_arrs[2]:
                    if rou_nai_num >= 7:
                        msg = '团本编号：' + code + "，T已满员，报名失败！"
                        await cmd2.finish(Message(f'{msg}'), reply_message=True)
                    else:
                        if rou_nai_num == 6:
                            if nei_wai_num >= 19:
                                msg = '团本编号：' + code + "，T已满员，报名失败！"
                                await cmd2.finish(Message(f'{msg}'), reply_message=True)
                        elif rou_nai_num == 5:
                            if nei_wai_num >= 20:
                                msg = '团本编号：' + code + "，T已满员，报名失败！"
                                await cmd2.finish(Message(f'{msg}'), reply_message=True)
                elif sect in sect_arrs[3]:
                    if rou_nai_num >= 7:
                        msg = '团本编号：' + code + "，奶妈已满员，报名失败！"
                        await cmd2.finish(Message(f'{msg}'), reply_message=True)
                    else:
                        if rou_nai_num == 6:
                            if nei_wai_num >= 19:
                                msg = '团本编号：' + code + "，奶妈已满员，报名失败！"
                                await cmd2.finish(Message(f'{msg}'), reply_message=True)
                        elif rou_nai_num == 5:
                            if nei_wai_num >= 20:
                                msg = '团本编号：' + code + "，奶妈已满员，报名失败！"
                                await cmd2.finish(Message(f'{msg}'), reply_message=True)
                else:
                    msg = '命令错误，请传入正确的门派！'
                    await cmd2.finish(Message(f'{msg}'), reply_message=True)

                data_json[code]["用户列表"].append(temp_json)
            else:
                msg = '命令错误，报名的团本编号不存在，请先确认团本列表，命令：/团本列表'
                await cmd2.finish(Message(f'{msg}'), reply_message=True)

        # 将处理后的JSON数据写入文件
        with open(data_path, 'w', encoding="utf-8") as f:
            json.dump(data_json, f, ensure_ascii=False)

        await cmd2.send('报名成功~', reply_message=True)

        data_json[code]["编号"] = code

        dir_path = Path(__file__).parent
        file_path = dir_path / "html" / "index.html"

        async with get_new_page(viewport={"width": 1100, "height": 100}) as page:
            await page.goto(
                "file://" + str(file_path.resolve()),
                timeout=2 * 60 * 1000,
                wait_until="networkidle",
            )
            await page.eval_on_selector('html', "load_data('{}')".format(json.dumps(data_json[code])))
            await asyncio.sleep(1)
            temp_path = "./data/jx3_open_group/index" + await get_current_timestamp_seconds() + ".png"
            pic = await page.screenshot(full_page=True, path=temp_path)

        await cmd2.finish(MessageSegment.image(pic))
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '报名失败！（请看后台日志排查问题）'
        await cmd2.finish(Message(f'{msg}'), reply_message=True)


# 取消报名 <团本编号>
@cmd3.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    group_id = event.group_id

    data_path = await check_data_file(group_id)

    # 命令校验
    if content == "":
        msg = '命令错误，请传入团本编号，命令：/取消报名 <团本编号>'
        await cmd3.finish(Message(f'{msg}'), reply_message=True)

    if not content.isdigit():
        msg = '命令错误，请传入正确的团本编号（纯数字），命令：/取消报名 <团本编号>'
        await cmd3.finish(Message(f'{msg}'), reply_message=True)

    try:
        data_json = None
        flag = False

        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)
        
            # 如果是空数据
            if len(data_json) == 0:
                msg = '当前不存在团本数据，请先开团报名后，再考虑删除。'
                await cmd3.finish(Message(f'{msg}'), reply_message=True)

            qq = event.get_user_id()

            users = data_json[content]['用户列表'] # 获取对应编号的用户列表
            for user in reversed(users):
                if user['QQ'] == qq: # 判断用户列表中是否存在该 QQ 号
                    users.remove(user) # 如果存在，则删除该用户
                    flag = True
                    break

        if flag:
            # 将处理后的JSON数据写入文件
            with open(data_path, 'w', encoding="utf-8") as f:
                json.dump(data_json, f, ensure_ascii=False)

            msg = "取消报名成功~"
            await cmd3.send(Message(f'{msg}'), reply_message=True)

            dir_path = Path(__file__).parent
            file_path = dir_path / "html" / "index.html"

            async with get_new_page(viewport={"width": 1100, "height": 100}) as page:
                await page.goto(
                    "file://" + str(file_path.resolve()),
                    timeout=2 * 60 * 1000,
                    wait_until="networkidle",
                )
                await page.eval_on_selector('html', "load_data('{}')".format(json.dumps(data_json[content])))
                await asyncio.sleep(1)
                temp_path = "./data/jx3_open_group/index" + await get_current_timestamp_seconds() + ".png"
                pic = await page.screenshot(full_page=True, path=temp_path)

            await cmd3.finish(MessageSegment.image(pic))
        else:
            msg = '您尚未报名此团本，无需删除。'
            await cmd3.finish(Message(f'{msg}'), reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '取消报名失败！（请看后台日志排查问题）'
        await cmd3.finish(Message(f'{msg}'), reply_message=True)


# 取消报名2 <团本编号>
@cmd10.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    group_id = event.group_id

    data_path = await check_data_file(group_id)

    # 命令校验
    if content == "":
        msg = '命令错误，请传入团本编号，命令：/取消报名2 <团本编号>'
        await cmd10.finish(Message(f'{msg}'), reply_message=True)

    if not content.isdigit():
        msg = '命令错误，请传入正确的团本编号（纯数字），命令：/取消报名2 <团本编号>'
        await cmd10.finish(Message(f'{msg}'), reply_message=True)

    try:
        data_json = None
        flag = False

        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)
        
            # 如果是空数据
            if len(data_json) == 0:
                msg = '当前不存在团本数据，请先开团报名后，再考虑删除。'
                await cmd10.finish(Message(f'{msg}'), reply_message=True)

            qq = event.get_user_id()

            users = data_json[content]['用户列表'] # 获取对应编号的用户列表
            for user in users:
                if user['QQ'] == qq: # 判断用户列表中是否存在该 QQ 号
                    users.remove(user) # 如果存在，则删除该用户
                    flag = True
                    break

        if flag:
            # 将处理后的JSON数据写入文件
            with open(data_path, 'w', encoding="utf-8") as f:
                json.dump(data_json, f, ensure_ascii=False)

            msg = "取消报名成功~"
            await cmd10.send(Message(f'{msg}'), reply_message=True)

            dir_path = Path(__file__).parent
            file_path = dir_path / "html" / "index.html"

            async with get_new_page(viewport={"width": 1100, "height": 100}) as page:
                await page.goto(
                    "file://" + str(file_path.resolve()),
                    timeout=2 * 60 * 1000,
                    wait_until="networkidle",
                )
                await page.eval_on_selector('html', "load_data('{}')".format(json.dumps(data_json[content])))
                await asyncio.sleep(1)
                temp_path = "./data/jx3_open_group/index" + await get_current_timestamp_seconds() + ".png"
                pic = await page.screenshot(full_page=True, path=temp_path)

            await cmd10.finish(MessageSegment.image(pic))
        else:
            msg = '您尚未报名此团本，无需删除。'
            await cmd10.finish(Message(f'{msg}'), reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '取消报名失败！（请看后台日志排查问题）'
        await cmd10.finish(Message(f'{msg}'), reply_message=True)


# 结束团本 <团本编号>
@cmd4.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    qq = event.get_user_id()
    group_id = event.group_id

    # bot = get_bot()
    # 获取群组信息
    group_info = await bot.get_group_member_list(group_id=group_id)  
    admins_info = []

    # print(group_info)
    for user_info in group_info:
        if user_info["role"] == "owner" or user_info["role"] == "admin":
            admins_info.append(user_info["user_id"])
    # print(admins_info)

    data_path = await check_data_file(group_id)

    # 命令校验
    if content == "":
        msg = '命令错误，请传入团本编号，命令：/结束团本 <团本编号>'
        await cmd4.finish(Message(f'{msg}'), reply_message=True)

    if not content.isdigit():
        msg = '命令错误，请传入正确的团本编号（纯数字），命令：/结束团本 <团本编号>'
        await cmd4.finish(Message(f'{msg}'), reply_message=True)

    try:
        data_json = None
        flag = False

        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)
        
            # 如果是空数据
            if len(data_json) == 0:
                msg = '当前不存在团本数据，请先开团后，再考虑删除。'
                await cmd4.finish(Message(f'{msg}'), reply_message=True)

            # 初始化标识符
            flag = False

            # 遍历字典，判断键名是否匹配
            for key in list(data_json.keys()):
                if content == key:
                    # 超级管理员可以直接执行，配置.env.xx文件中
                    if qq not in global_config.superusers and qq not in admins_info:
                        # 判断用户是否是团本创始人
                        if qq == data_json[key]["创始人QQ"]:
                            del data_json[key] # 如果匹配，则删除该键值对
                            flag = True # 标识符置为 True
                        else:
                            msg = '您没有权限删除此团本。'
                            await cmd4.finish(Message(f'{msg}'), reply_message=True)
                    else:
                        del data_json[key] # 如果匹配，则删除该键值对
                        flag = True # 标识符置为 True

        if flag:
            # 将处理后的JSON数据写入文件
            with open(data_path, 'w', encoding="utf-8") as f:
                json.dump(data_json, f, ensure_ascii=False)

            msg = "结束团本成功~"
            await cmd4.send(Message(f'{msg}'), reply_message=True)

            dir_path = Path(__file__).parent
            file_path = dir_path / "html" / "list.html"

            async with get_new_page(viewport={"width": 1100, "height": 100}) as page:
                await page.goto(
                    "file://" + str(file_path.resolve()),
                    timeout=2 * 60 * 1000,
                    wait_until="networkidle",
                )
                await page.eval_on_selector('html', "load_data('{}')".format(json.dumps(data_json)))
                await asyncio.sleep(1)
                temp_path = "./data/jx3_open_group/list" + await get_current_timestamp_seconds() + ".png"
                pic = await page.screenshot(full_page=True, path=temp_path)

            await cmd4.finish(MessageSegment.image(pic))
        else:
            msg = '团本不存在，无需删除。'
            await cmd4.finish(Message(f'{msg}'), reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '结束团本失败！（请看后台日志排查问题）'
        await cmd4.finish(Message(f'{msg}'), reply_message=True)


# 团本列表
@cmd5.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id

    data_path = await check_data_file(group_id)

    await cmd5.send('获取团本数据中，请稍后...', reply_message=True)
    try:
        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)
        
            dir_path = Path(__file__).parent
            file_path = dir_path / "html" / "list.html"

            async with get_new_page(viewport={"width": 1100, "height": 100}) as page:
                await page.goto(
                    "file://" + str(file_path.resolve()),
                    timeout=2 * 60 * 1000,
                    wait_until="networkidle",
                )
                await page.eval_on_selector('html', "load_data('{}')".format(json.dumps(data_json)))
                await asyncio.sleep(1)
                temp_path = "./data/jx3_open_group/list" + await get_current_timestamp_seconds() + ".png"
                pic = await page.screenshot(full_page=True, path=temp_path)

            await cmd5.finish(MessageSegment.image(pic))
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '查看团本列表失败！（请看后台日志排查问题）'
        await cmd5.finish(Message(f'{msg}'), reply_message=True)


# 查团 <团本编号>
@cmd6.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    group_id = event.group_id

    data_path = await check_data_file(group_id)
    
    if content == "":
        msg = '命令错误，请传入团本编号，命令：/查团 <团本编号>'
        await cmd6.finish(Message(f'{msg}'), reply_message=True)

    if not content.isdigit():
        msg = '命令错误，请传入正确的团本编号（纯数字），命令：/查团 <团本编号>'
        await cmd6.finish(Message(f'{msg}'), reply_message=True)

    data_json = {}

    await cmd6.send('查询中，请稍后...', reply_message=True)

    try:
        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)
        
            # 如果是空数据
            if len(data_json) == 0:
                await cmd6.finish('没有团本数据，请先开团。', reply_message=True)

        if content in data_json:
            dir_path = Path(__file__).parent
            file_path = dir_path / "html" / "index.html"

            async with get_new_page(viewport={"width": 1100, "height": 100}) as page:
                await page.goto(
                    "file://" + str(file_path.resolve()),
                    timeout=2 * 60 * 1000,
                    wait_until="networkidle",
                )
                await page.eval_on_selector('html', "load_data('{}')".format(json.dumps(data_json[content])))
                await asyncio.sleep(1)
                temp_path = "./data/jx3_open_group/index" + await get_current_timestamp_seconds() + ".png"
                pic = await page.screenshot(full_page=True, path=temp_path)

            await cmd6.finish(MessageSegment.image(pic))
        else:
            await cmd6.finish('您查询的团本不存在，请先查询团本列表确认团本编号。', reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '查询团本失败！（请看后台日志排查问题）'
        await cmd6.finish(Message(f'{msg}'), reply_message=True)


# 开除团队 <团本编号> <对象ID/QQ>
@cmd7.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    content = content.split()

    group_id = event.group_id

    data_path = await check_data_file(group_id)

    # 命令校验
    if len(content) < 2:
        msg = '命令错误，请传入团本编号和要删除用户的ID/QQ，命令：/开除团队 <团本编号> <对象ID/QQ>'
        await cmd7.finish(Message(f'{msg}'), reply_message=True)

    if not content[0].isdigit():
        msg = '命令错误，请传入纯数字的团本编号，命令：/开除团队 <团本编号> <对象ID/QQ>'
        await cmd7.finish(Message(f'{msg}'), reply_message=True)

    try:
        data_json = None

        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)
        
            # 如果是空数据
            if len(data_json) == 0:
                msg = '当前不存在团本数据，请先开团后，再考虑删除。'
                await cmd7.finish(Message(f'{msg}'), reply_message=True)

            last_matched_user = None

            # 遍历字典，判断键名是否匹配
            for key in list(data_json.keys()):
                if content[0] == key:
                    for user in reversed(data_json[key]["用户列表"]):
                        # 匹配ID或QQ
                        if content[1] == user["ID"] or content[1] == user["QQ"]:
                            last_matched_user = user
                            break  # 匹配到用户以后退出循环，避免后续操作

                    if last_matched_user is not None:
                        data_json[key]["用户列表"].remove(last_matched_user)
                    else:
                        msg = '当前团本不存在此用户信息，无需删除。'
                        await cmd7.finish(Message(f'{msg}'), reply_message=True)
            
            if last_matched_user is None:
                msg = '不存在此团本，无需删除。'
                await cmd7.finish(Message(f'{msg}'), reply_message=True)
            
            
        # 将处理后的JSON数据写入文件
        with open(data_path, 'w', encoding="utf-8") as f:
            json.dump(data_json, f, ensure_ascii=False)

        msg = "删除用户报名信息成功~"
        await cmd7.send(Message(f'{msg}'), reply_message=True)

        dir_path = Path(__file__).parent
        file_path = dir_path / "html" / "index.html"

        async with get_new_page(viewport={"width": 1100, "height": 100}) as page:
            await page.goto(
                "file://" + str(file_path.resolve()),
                timeout=2 * 60 * 1000,
                wait_until="networkidle",
            )
            await page.eval_on_selector('html', "load_data('{}')".format(json.dumps(data_json[content[0]])))
            await asyncio.sleep(1)
            temp_path = "./data/jx3_open_group/index" + await get_current_timestamp_seconds() + ".png"
            pic = await page.screenshot(full_page=True, path=temp_path)

        await cmd7.finish(MessageSegment.image(pic))
    except FinishedException:
        pass
    except Exception as e:
        # 打印完整的堆栈信息
        traceback.print_exc()  
        logger.info(e)
        msg = '删除用户报名信息失败！（请看后台日志排查问题）'
        await cmd7.finish(Message(f'{msg}'), reply_message=True)


# 开除团队2 <团本编号> <对象ID/QQ>
@cmd11.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    content = content.split()

    group_id = event.group_id

    data_path = await check_data_file(group_id)

    # 命令校验
    if len(content) < 2:
        msg = '命令错误，请传入团本编号和要删除用户的ID/QQ，命令：/开除团队2 <团本编号> <对象ID/QQ>'
        await cmd11.finish(Message(f'{msg}'), reply_message=True)

    if not content[0].isdigit():
        msg = '命令错误，请传入纯数字的团本编号，命令：/开除团队2 <团本编号> <对象ID/QQ>'
        await cmd11.finish(Message(f'{msg}'), reply_message=True)

    try:
        data_json = None

        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)
        
            # 如果是空数据
            if len(data_json) == 0:
                msg = '当前不存在团本数据，请先开团后，再考虑删除。'
                await cmd11.finish(Message(f'{msg}'), reply_message=True)

            last_matched_user = None

            # 遍历字典，判断键名是否匹配
            for key in list(data_json.keys()):
                if content[0] == key:
                    for user in data_json[key]["用户列表"]:
                        if content[1] == user["ID"] or content[1] == user["QQ"]:
                            last_matched_user = user
                            break  # 匹配到用户以后退出循环，避免后续操作

                    if last_matched_user is not None:
                        data_json[key]["用户列表"].remove(last_matched_user)
                    else:
                        msg = '当前团本不存在此用户信息，无需删除。'
                        await cmd11.finish(Message(f'{msg}'), reply_message=True)
            
            if last_matched_user is None:
                msg = '不存在此团本，无需删除。'
                await cmd11.finish(Message(f'{msg}'), reply_message=True)
            
            
        # 将处理后的JSON数据写入文件
        with open(data_path, 'w', encoding="utf-8") as f:
            json.dump(data_json, f, ensure_ascii=False)

        msg = "删除用户报名信息成功~"
        await cmd11.send(Message(f'{msg}'), reply_message=True)

        dir_path = Path(__file__).parent
        file_path = dir_path / "html" / "index.html"

        async with get_new_page(viewport={"width": 1100, "height": 100}) as page:
            await page.goto(
                "file://" + str(file_path.resolve()),
                timeout=2 * 60 * 1000,
                wait_until="networkidle",
            )
            await page.eval_on_selector('html', "load_data('{}')".format(json.dumps(data_json[content[0]])))
            await asyncio.sleep(1)
            temp_path = "./data/jx3_open_group/index" + await get_current_timestamp_seconds() + ".png"
            pic = await page.screenshot(full_page=True, path=temp_path)

        await cmd11.finish(MessageSegment.image(pic))
    except FinishedException:
        pass
    except Exception as e:
        # 打印完整的堆栈信息
        traceback.print_exc()  
        logger.info(e)
        msg = '删除用户报名信息失败！（请看后台日志排查问题）'
        await cmd11.finish(Message(f'{msg}'), reply_message=True)


# 强制清空团本
@cmd8.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id

    data_path = await check_data_file(group_id)

    temp_json = {}

    try:
        # 将处理后的JSON数据写入文件
        with open(data_path, 'w', encoding="utf-8") as f:
            json.dump(temp_json, f, ensure_ascii=False)

        msg = '成功清空所有团本~'
        await cmd8.finish(Message(f'{msg}'), reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '清空所有团本失败！（请看后台日志排查问题）'
        await cmd8.finish(Message(f'{msg}'), reply_message=True)


# 强制删除所有报名 <团本编号>
@cmd9.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    group_id = event.group_id

    data_path = await check_data_file(group_id)

    # 命令校验
    if content == '':
        msg = '命令错误，请传入团本编号，命令：/强制删除所有报名 <团本编号>'
        await cmd9.finish(Message(f'{msg}'), reply_message=True)

    if not content.isdigit():
        msg = '命令错误，请传入团本编号(纯数字)，命令：/强制删除所有报名 <团本编号>'
        await cmd9.finish(Message(f'{msg}'), reply_message=True)

    try:
        data_json = None
        flag = False

        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)
        
            # 如果是空数据
            if len(data_json) == 0:
                msg = '当前不存在团本数据，请先开团后，再考虑删除。'
                await cmd9.finish(Message(f'{msg}'), reply_message=True)

            # 遍历字典，判断键名是否匹配
            for key in list(data_json.keys()):
                if content[0] == key:
                    data_json[key]['用户列表'] = []
                    flag = True
            
            if flag == False:
                msg = '不存在此团本，无需删除。'
                await cmd9.finish(Message(f'{msg}'), reply_message=True)
               
        # 将处理后的JSON数据写入文件
        with open(data_path, 'w', encoding="utf-8") as f:
            json.dump(data_json, f, ensure_ascii=False)

        msg = "删除所有用户报名信息成功~"
        await cmd9.finish(Message(f'{msg}'), reply_message=True)

        # 没必要返回图了，反正也是空数据
        dir_path = Path(__file__).parent
        file_path = dir_path / "html" / "index.html"

        async with get_new_page(viewport={"width": 1100, "height": 100}) as page:
            await page.goto(
                "file://" + str(file_path.resolve()),
                timeout=2 * 60 * 1000,
                wait_until="networkidle",
            )
            await page.eval_on_selector('html', "load_data('{}')".format(json.dumps(data_json[content[0]])))
            await asyncio.sleep(1)
            temp_path = "./data/jx3_open_group/index" + await get_current_timestamp_seconds() + ".png"
            pic = await page.screenshot(full_page=True, path=temp_path)

        await cmd9.finish(MessageSegment.image(pic))
    except FinishedException:
        pass
    except Exception as e:
        # 打印完整的堆栈信息
        traceback.print_exc()  
        logger.info(e)
        msg = '删除所有用户报名信息失败！（请看后台日志排查问题）'
        await cmd9.finish(Message(f'{msg}'), reply_message=True)


# 获取时间戳的 年月日时分秒
async def get_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


# 获取时间戳的当前的秒
async def get_current_timestamp_seconds():
    current_timestamp = int(time.time())
    return str(current_timestamp % 60)


# 检查数据文件 传入群号
async def check_data_file(group_id):
    data_path = data_dir + "/data_" + str(group_id) + ".json"

    # 创建目录
    os.makedirs(root_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    # 如果文件不存在，则创建新文件
    if not os.path.exists(data_path):
        with open(data_path, 'w') as f:
            json.dump({}, f)

    return data_path

