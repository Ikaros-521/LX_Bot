from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg
import re, io
import json
import aiohttp
import nonebot

# 配合https://github.com/Plachtaa/VITS-fast-fine-tuning 使用

# vits配置文件路径(注意路径转义问题)
config_path = "E:\\GitHub_pro\\VITS-fast-fine-tuning\\inference\\finetune_speaker.json"
# api的ip和端口，注意书写格式
api_ip_port = "127.0.0.1:7860"

catch_str = on_command("VITS", aliases={"vits"})

@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        nonebot.logger.error(e)
        await catch_str.finish('加载配置文件失败，请进行修复', at_sender=True)

    speakers = data["speakers"]

    content = msg.extract_plain_text().strip()

    content = content.split()

    character = "ikaros"
    language = "中文"
    text = "这是默认合成内容"
    speed = 1

    if len(content) == 2:
        character = content[0]
        text = content[1]
    elif len(content) == 3:
        character = content[0]
        language = content[1]
        text = content[2]
    elif len(content) == 4:
        character = content[0]
        language = content[1]
        speed = float(content[2])
        text = content[3]
    elif len(content) == 1:
        msg = '命令错误，命令格式：【/vits 角色名 语言 合成内容】'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    else:
        msg = '命令错误(合成内容不要有空格)，命令格式：【/vits 角色名 语言 合成内容】'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    # 是数字则是获取json对应的key
    if character.isdigit():
        desired_value = int(character)
        for key, value in speakers.items():
            if value == desired_value:
                character = key

    data_json = await get_data(character, language, text, speed)

    # print(data_json)

    try:
        name = data_json["data"][1]["name"]
        # 请求文件地址获取返回形式
        # file_data = await get_file(name)

        # 直接传入文件url
        file_path = 'http://' + api_ip_port + '/file=' + name
        await catch_str.send(MessageSegment.record(file=file_path))

        # 本地打开文件
        # file = open(name, 'br')  # 使用二进制
        # io_file = io.BytesIO(file.read())  # 使用BytesIO读取
        # await catch_str.send(MessageSegment.record(file=io_file))
    except:
        msg = '发送音频失败，请检查接口是否正常'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_file(name):
    # API地址
    API_URL = 'http://' + api_ip_port + '/file=' + name

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
                # print(result)
        return ret
    except Exception as e:
        nonebot.logger.info(e)
        return None


async def get_data(character="ikaros", language="日语", text="こんにちわ。", speed=1):
    # API地址
    API_URL = 'http://' + api_ip_port + '/run/predict/'

    data_json = {
        "fn_index":0,
        "data":[
            "こんにちわ。",
            "ikaros",
            "日本語",
            1
        ],
        "session_hash":"mnqeianp9th"
    }

    if language == "中文" or language == "汉语":
        data_json["data"] = [text, character, "简体中文", speed]
    elif language == "英文" or language == "英语":
        data_json["data"] = [text, character, "English", speed]
    else:
        data_json["data"] = [text, character, "日本語", speed]

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=API_URL, json=data_json) as response:
                result = await response.read()
                # print(result)
                ret = json.loads(result)
        return ret
    except Exception as e:
        nonebot.logger.info(e)
        return None
    

async def get_data_from_hf(character="ikaros", language="日语", text="こんにちわ。", speed=1):
    # API地址
    API_URL = 'http://' + api_ip_port + '/run/predict/'

    data_json = {
        "fn_index":0,
        "data":[
            "こんにちわ。",
            "ikaros",
            "日本語",
            1
        ],
        "session_hash":"mnqeianp9th"
    }

    if language == "中文" or language == "汉语":
        data_json["data"] = [text, character, "简体中文", speed]
    # elif language == "英文" or language == "英语":
    #     data_json["data"] = [text, character, "English", speed]
    else:
        data_json["data"] = [text, character, "日本語", speed]

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=API_URL, json=data_json) as response:
                result = await response.read()
                # print(result)
                ret = json.loads(result)
        return ret
    except Exception as e:
        nonebot.logger.info(e)
        return None
    