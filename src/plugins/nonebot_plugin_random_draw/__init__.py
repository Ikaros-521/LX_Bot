import json
import random
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
from nonebot.typing import T_State

from nonebot.plugin import PluginMetadata


help_text = f"""
功能说明：命令列表（命令前缀自行匹配）
获取帮助：随机抽取帮助
创建随抽组，一个群可以有多个组：随抽组创建 <组名>
往指定的随抽组中添加待抽内容（可多个，用空格分隔）：随抽添加 <组号> <内容>
删除指定随抽组中的待抽内容（可多个，用空格分隔）：随抽删除 <组号> <内容>
删除指定组号的随抽组：随抽组删除 <组号>
查看本群所有的随抽组内容（含组号和组名）：随抽组列表
查看指定组号的所有待抽内容：随抽列表 <组号>
在指定随抽组中随机抽取一个待抽内容：随抽 <组号>
清空本群中所有的随抽组（慎用）：随抽组清空
清空指定随抽组中所有的待抽内容（慎用）：随抽清空 <组号>


注意：
随抽内容必须配合文本描述，不能只是图片。
批量添加待抽内容不支持图片批量，如果你硬这么用，就都是重复的图片。
随抽删除只需要传入文本内容即可，不需要图片。
查看随抽列表只返回文本内容。
图片用的是tx的图床，所以一段时间后会挂。
""".strip()

__plugin_meta__ = PluginMetadata(
    name = '随机抽取设定内容插件',
    description = '适用于nonebot2 v11的随机抽取设定内容插件',
    usage = help_text
)


superuser = []
global_config = nonebot.get_driver().config

# 数据存储路径
root_dir = "data"
data_dir = root_dir + "/nonebot_plugin_random_draw"
data_path = ""

cmd0 = on_command("随抽帮助", aliases={"随机抽取组创建"})
cmd1 = on_command("随抽组创建", aliases={"随机抽取组创建"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
cmd2 = on_command("随抽添加", aliases={"随机抽取添加"})
cmd3 = on_command("随抽删除", aliases={"随机抽取删除"})
cmd4 = on_command("随抽组删除", aliases={"随机抽取组删除"})
cmd5 = on_command("随抽组列表", aliases={"随机抽取组列表"})
cmd6 = on_command("随抽列表", aliases={"随机抽取列表"})
cmd7 = on_command("随抽", aliases={"随机抽取"})
cmd8 = on_command("随抽组清空", aliases={"随机抽取组清空"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
cmd9 = on_command("随抽清空", aliases={"随机抽取清空"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


# 随机抽取帮助
@cmd0.handle()
async def _(bot: Bot, event: Event):
    # cur_path = os.path.abspath(__file__)
    # 获取当前脚本所在目录的路径
    # dir_path = os.path.dirname(cur_path)
    # print(dir_path)
    # img_path = Path(dir_path + '/html/img/help.png')
    # print(img_path)

    await cmd0.finish(help_text)


# 随抽组创建 <组名>
@cmd1.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    qq = event.get_user_id()
    group_id = event.group_id

    data_path = await check_data_file(group_id)
    
    if content == "":
        msg = '命令错误，请传入团本描述，命令：/随抽组创建 <组名>'
        await cmd1.finish(Message(f'{msg}'), reply_message=True)

    data_json = {}
    new_last_key = 0

    # 待插入文件的数据
    temp_json = {
        "标题": content,
        "创始人QQ": qq,
        "创建时间": await get_current_datetime(),
        "内容": [
        ]
    }

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
            temp_json["组号"] = new_last_key

        # 将处理后的JSON数据写入文件
        with open(data_path, 'w', encoding="utf-8") as f:
            json.dump(data_json, f, ensure_ascii=False)

        # 注释下行的话，可以返回开团图
        msg = '创建成功。组号：' + str(new_last_key)
        await cmd1.finish(msg, reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '创建失败！（请看后台日志排查问题）'
        await cmd1.finish(Message(f'{msg}'), reply_message=True)


# 随抽添加 <组号> <内容>
@cmd2.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    content = content.split()

    print(content)

    if msg:
        state["src_img"] = msg
    pass

    # 获取图片部分
    event_msg = event.get_plaintext()
    event_msg: Message = state["src_img"]

    # 暂时先拿tx当图床吧
    img_url = ""

    for msg_sag in event_msg:
        if msg_sag.type == "image":
            img_url = msg_sag.data["url"]
            break

    group_id = event.group_id

    data_path = await check_data_file(group_id)

    if len(content) < 2:
        msg = '命令错误，命令：/随抽添加 <组号> <内容>'
        await cmd2.finish(Message(f'{msg}'), reply_message=True)


    group_num = content[0]
    # 删除组号
    del content[0]
    # content_str = content[1]
    # qq = event.get_user_id()

    data_json = {}

    try:
        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)
        
            # 判断是否存在
            if group_num not in data_json:
                msg = "不存在此随抽组，请先创建随抽组。"
                await cmd2.send(Message(f'{msg}'), reply_message=True)

            data_arr = []

            for data in content:
                flag = 0
                for tmp_data in data_json[group_num]["内容"]:
                    # 重复性检测
                    if tmp_data['文本'] == data:
                        # print(f"{data}重复")
                        data_arr.append(data)

                        flag = 1
                        break

                if flag == 0:
                    tmp = {"文本": data, "图片": img_url}
                    data_json[group_num]["内容"].append(tmp)
                    print(f"追加{json.dumps(tmp)}")
            
            if len(data_arr) != 0:
                msg = '组号：' + group_num + "，已存在 "
                for data in data_arr:
                    msg = msg + data + " "
                msg = msg + "，请勿重复添加！"
                await cmd2.send(Message(f'{msg}'), reply_message=True)

        # 将处理后的JSON数据写入文件
        with open(data_path, 'w', encoding="utf-8") as f:
            json.dump(data_json, f, ensure_ascii=False)

        await cmd2.finish('添加成功~', reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '添加失败！（请看后台日志排查问题）'
        await cmd2.finish(Message(f'{msg}'), reply_message=True)


# 随抽删除 <组号> <内容>
@cmd3.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    group_id = event.group_id

    content = content.split()

    data_path = await check_data_file(group_id)

    if len(content) < 2:
        msg = '命令错误，命令：/随抽删除 <组号> <内容>'
        await cmd2.finish(Message(f'{msg}'), reply_message=True)

    group_num = content[0]
    # content_str = content[1]
    del content[0]

    try:
        data_json = None

        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)
        
            # 判断键是否存在
            if group_num not in data_json:
                msg = '当前不存在随抽组，请先创建随抽组后，再考虑删除。'
                await cmd3.finish(Message(f'{msg}'), reply_message=True)

            # 如果是空数据
            if len(data_json[group_num]) == 0:
                msg = '当前随抽组无内容，无需删除。'
                await cmd3.finish(Message(f'{msg}'), reply_message=True)

            # qq = event.get_user_id()

            for content_str in content:
                for text_and_img in data_json[group_num]["内容"]:
                    if content_str == text_and_img["文本"]:
                        data_json[group_num]["内容"].remove(text_and_img)
                        # 将处理后的JSON数据写入文件
                        with open(data_path, 'w', encoding="utf-8") as f:
                            json.dump(data_json, f, ensure_ascii=False)

            msg = "随抽删除匹配的内容成功~"
            await cmd3.send(Message(f'{msg}'), reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '随抽删除失败！（请看后台日志排查问题）'
        await cmd3.finish(Message(f'{msg}'), reply_message=True)


# 随抽组删除 <组号>
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
        msg = '命令错误，请传入组号，命令：/随抽组删除 <组号>'
        await cmd4.finish(Message(f'{msg}'), reply_message=True)

    if not content.isdigit():
        msg = '命令错误，请传入正确的组号（纯数字），命令：/随抽组删除 <组号>'
        await cmd4.finish(Message(f'{msg}'), reply_message=True)

    try:
        data_json = None
        flag = False

        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)

            # 判断键是否存在
            if content not in data_json:
                msg = '当前不存在随抽组，请先创建随抽组后，再考虑删除。'
                await cmd4.finish(Message(f'{msg}'), reply_message=True)
        
            # 如果是空数据
            if len(data_json) == 0:
                msg = '当前不存在随抽组，请先创建随抽组后，再考虑删除。'
                await cmd4.finish(Message(f'{msg}'), reply_message=True)

            # 初始化标识符
            flag = False

            # 遍历字典，判断键名是否匹配
            for key in list(data_json.keys()):
                if content == key:
                    # 超级管理员可以直接执行，配置.env.xx文件中
                    if qq not in global_config.superusers and qq not in admins_info:
                        # 判断用户是否是随抽组创始人
                        if qq == data_json[key]["创始人QQ"]:
                            del data_json[key] # 如果匹配，则删除该键值对
                            flag = True # 标识符置为 True
                        else:
                            msg = '您没有权限删除此随抽组。'
                            await cmd4.finish(Message(f'{msg}'), reply_message=True)
                    else:
                        del data_json[key] # 如果匹配，则删除该键值对
                        flag = True # 标识符置为 True

        if flag:
            # 将处理后的JSON数据写入文件
            with open(data_path, 'w', encoding="utf-8") as f:
                json.dump(data_json, f, ensure_ascii=False)

            msg = "删除随抽组成功~"
            await cmd4.finish(Message(f'{msg}'), reply_message=True)
        else:
            msg = '随抽组不存在，无需删除。'
            await cmd4.finish(Message(f'{msg}'), reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '删除随抽组失败！（请看后台日志排查问题）'
        await cmd4.finish(Message(f'{msg}'), reply_message=True)


# 随抽组列表
@cmd5.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id

    data_path = await check_data_file(group_id)

    try:
        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)

            msg = "随抽组编号列表：\n组号   标题\n"

            for key in list(data_json.keys()):
                msg = msg + str(key) + '        ' + data_json[key]['标题'] + '\n'

            await cmd5.finish(msg)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '查看随抽组列表失败！（请看后台日志排查问题）'
        await cmd5.finish(Message(f'{msg}'), reply_message=True)


# 随抽列表 <组号>
@cmd6.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    group_id = event.group_id

    data_path = await check_data_file(group_id)
    
    if content == "":
        msg = '命令错误，请传入组号，命令：/随抽列表 <组号>'
        await cmd6.finish(Message(f'{msg}'), reply_message=True)

    if not content.isdigit():
        msg = '命令错误，请传入正确的组号（纯数字），命令：/随抽列表 <组号>'
        await cmd6.finish(Message(f'{msg}'), reply_message=True)

    data_json = {}

    try:
        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)

            # 判断键是否存在
            if content not in data_json:
                msg = '没有此随抽组，请先创建。'
                await cmd6.finish(Message(f'{msg}'), reply_message=True)
        
            # 如果是空数据
            if len(data_json) == 0:
                await cmd6.finish('没有随抽组，请先创建。', reply_message=True)

        if content in data_json:
            msg = "内容(图片不展示)：\n"
            for data in data_json[content]['内容']:
                msg = msg + data['文本'] + '\n'
            await cmd6.finish(msg)
        else:
            await cmd6.finish('您查询的随抽组不存在，请先查询随抽组列表确认组号。', reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '查询随抽列表失败！（请看后台日志排查问题）'
        await cmd6.finish(Message(f'{msg}'), reply_message=True)

# 随抽 <组号>
@cmd7.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    group_id = event.group_id

    data_path = await check_data_file(group_id)
    
    if content == "":
        msg = '命令错误，请传入组号，命令：/随抽 <组号>'
        await cmd7.finish(Message(f'{msg}'), reply_message=True)

    if not content.isdigit():
        msg = '命令错误，请传入正确的组号（纯数字），命令：/随抽 <组号>'
        await cmd7.finish(Message(f'{msg}'), reply_message=True)

    data_json = {}

    try:
        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)

            # 判断键是否存在
            if content not in data_json:
                msg = '没有此随抽组，请先创建。'
                await cmd7.finish(Message(f'{msg}'), reply_message=True)
        
            # 如果是空数据
            if len(data_json) == 0:
                await cmd7.finish('没有随抽组，请先创建。', reply_message=True)

        if 0 != len(data_json[content]['内容']):
            # 随机抽一个
            index = random.randint(0, len(data_json[content]['内容']) - 1)
            text_seg = MessageSegment.text(data_json[content]['内容'][index]['文本'])
            if data_json[content]['内容'][index]['图片'] != "":
                img_seg = MessageSegment.image(file=data_json[content]['内容'][index]['图片'])
                await cmd7.finish(Message(text_seg + img_seg))
            else:
                await cmd7.finish(Message(text_seg))
        else:
            await cmd7.finish('您抽的随抽组无内容，请先添加内容。', reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '随抽失败！（请看后台日志排查问题）'
        await cmd7.finish(Message(f'{msg}'), reply_message=True)


# 随抽组清空
@cmd8.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id

    data_path = await check_data_file(group_id)

    temp_json = {}

    try:
        # 将处理后的JSON数据写入文件
        with open(data_path, 'w', encoding="utf-8") as f:
            json.dump(temp_json, f, ensure_ascii=False)

        msg = '成功清空所有随抽组~'
        await cmd8.finish(Message(f'{msg}'), reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        logger.info(e)
        msg = '清空所有随抽组失败！（请看后台日志排查问题）'
        await cmd8.finish(Message(f'{msg}'), reply_message=True)


# 随抽清空 <组号>
@cmd9.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    group_id = event.group_id

    data_path = await check_data_file(group_id)

    # 命令校验
    if content == '':
        msg = '命令错误，请传入组号，命令：/随抽清空 <组号>'
        await cmd9.finish(Message(f'{msg}'), reply_message=True)

    if not content.isdigit():
        msg = '命令错误，请传入组号(纯数字)，命令：/随抽清空 <组号>'
        await cmd9.finish(Message(f'{msg}'), reply_message=True)

    try:
        data_json = None
        flag = False

        # 打开JSON文件
        with open(data_path, 'r', encoding="utf-8") as f:
            # 读取文件内容并解析JSON
            data_json = json.load(f)

            # 判断键是否存在
            if content not in data_json:
                msg = '没有此随抽组，请先创建。'
                await cmd9.finish(Message(f'{msg}'), reply_message=True)
        
            # 如果是空数据
            if len(data_json) == 0:
                msg = '当前不存在随抽组，请先创建随抽组后，再考虑删除。'
                await cmd9.finish(Message(f'{msg}'), reply_message=True)

            # 遍历字典，判断键名是否匹配
            for key in list(data_json.keys()):
                if content[0] == key:
                    data_json[key]['内容'] = []
                    flag = True
            
            if flag == False:
                msg = '不存在此随抽组，无需删除。'
                await cmd9.finish(Message(f'{msg}'), reply_message=True)
               
        # 将处理后的JSON数据写入文件
        with open(data_path, 'w', encoding="utf-8") as f:
            json.dump(data_json, f, ensure_ascii=False)

        msg = "删除所有随抽信息成功~"
        await cmd9.finish(Message(f'{msg}'), reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        # 打印完整的堆栈信息
        traceback.print_exc()  
        logger.info(e)
        msg = '删除所有随抽信息失败！（请看后台日志排查问题）'
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

