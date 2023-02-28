import nonebot
import aiohttp, time
from nonebot import on_command, on_shell_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import (
    Bot, 
    # Event,
    GroupMessageEvent,
    Message,
    MessageSegment,
    MessageEvent,
    # PrivateMessageEvent,
)
from nonebot.params import CommandArg, ShellCommandArgs
from argparse import Namespace 
from nonebot.rule import ArgumentParser
from nonebot.plugin import PluginMetadata
from pathlib import Path
import io
import numpy as np
from PIL import Image
from nonebot.exception import FinishedException


help_text = f"""
①默认配置的背景消除
1、先发送命令，再发送图片（命令前缀请自行替换）
先发送`/去背景`或`/rm_bg`，等bot返回`请发送需要去除背景的图片喵~`后，发送需要去除背景的图片即可。  

2、命令+图片
编辑消息`/去背景[待去除背景的图片]`或`/rm_bg[待去除背景的图片]`发送即可。  

3、回复图片+命令
回复需要处理的图片，然后追加命令`/去背景`或`/rm_bg`发送即可。

②自定义配置的背景消除
命令如下(命令前缀自行添加)：  
自定义去背景 -img <IMAGE> [-s --size -最大输出分辨率 <最大输出图像分辨率 'preview/full/auto'>] [-t --type -前景类型 <前景类型 'auto/person/product/car'>] [-tl --type_level -前景类型级别 <检测到的前景类型的分类级别 'none/1/2/latest'>]\n [-r --roi -感兴趣区域 <感兴趣区域 x1 y1 x2 y2，如'0% 0% 100% 100%'>] [-c --crop -裁剪空白区 <是否裁剪掉所有空白区域 'true/false'>] [-p --position -定位主题 <在图像画布中定位主题 'center/original/从“0%”到“100%”的一个值(水平和垂直)或两个值(水平、垂直)'>]\n [-sc --scale -缩放主体 <相对于图像总尺寸缩放主体 从“10%”到“100%”之间的任何值，也可以是“original”(默认)。缩放主体意味着“位置=中心”(除非另有说明)。>] [-ad --add_shadow -人工阴影 <是否向结果添加人工阴影 'true/false'>] [-se --semitransparency -半透明区域 <结果中是否包含半透明区域 'true/false'>]

命令起始：`自定义去背景` 或 `remove_bg`  
`-img` 必选参数，后面追加`<IMAGE>`图片（回复的话，图片就不用了）  
`-s` 可选参数 `-s`可以改成 `--size` 或 `-最大输出分辨率`，含义是最大输出图像分辨率，传参内容是`'preview/full/auto'`（3选1）  
其他的[]都是可选参数，含义和-s相同，不再赘述。
例如：  
/自定义去背景 -img <IMAGE> -s 'preview'
/remove_bg -img <IMAGE> -s 'full' -r '30% 30% 60% 60%' -ad 'true'
/自定义去背景 -图片 <IMAGE> -最大输出分辨率 'preview' -前景类型 'person' -前景类型级别 '1' -感兴趣区域 '0% 0% 100% 100%' -裁剪空白区 'true' -定位主题 'center' -缩放主体 '50%' -人工阴影 'false'  -半透明区域 'false'
""".strip()

__plugin_meta__ = PluginMetadata(
    name = '图片背景消除',
    description = '基于remove.bg的图片背景消除插件',
    usage = help_text
)

# 官网获取 https://www.remove.bg/api#remove-background
remove_bg_api_key = ""

# 获取env配置
try:
    nonebot.logger.debug(nonebot.get_driver().config.remove_bg_api_key)
    remove_bg_api_key = nonebot.get_driver().config.remove_bg_api_key
except:
    nonebot.logger.warning("REMOVE_BG_API_KEY配置缺失喵，不配置功能无法使用滴~")

catch_str = on_command("去背景", aliases={"rm_bg"})
img_url = ""

@catch_str.handle()
async def _(state: T_State, event: MessageEvent, arg: Message = CommandArg()):
    global img_url
    # 回复图片
    reply = event.reply
    if reply:
        for seg in reply.message['image']:
            img_url = seg.data["url"]
            state["src_img"] = ""
        pass
    
    msg = arg
    if msg:
        state["src_img"] = msg
    pass


@catch_str.got("src_img", prompt="请发送需要去除背景的图片喵~")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    # 信息源自 群聊或私聊
    msg_from = "group"
    # 判断消息类型
    if not isinstance(event, GroupMessageEvent):
        msg_from = "private"
    
    url = ""
    # nonebot.logger.debug("img_url:" + img_url)
    if img_url == "":
        msg: Message = state["src_img"]
        # try:
        for msg_sag in msg:
            if msg_sag.type == "image":
                url = msg_sag.data["url"]
            else:
                await catch_str.finish("请发送图片喵~命令结束")
    else:
        url = img_url

    nonebot.logger.info("url:" + url)

    # 私聊的图片需要特殊处理
    if msg_from == "group":
        img_data = await remove_by_url(url, None)
    else:
        img_data = await remove_by_img(url, None)

    if img_data == None:
        msg = '请求出错，可能是网络问题或者API寄了喵~'
        await catch_str2.finish(Message(f'{msg}'), at_sender=True)
    
    # nonebot.logger.info(img_data)

    try:
        if msg_from == "group":
            dir_path = Path(__file__).parent
            file_path = dir_path / (await get_current_timestamp_seconds() + '.gif')
            file_path = str(file_path)
            
            png_image = Image.open(io.BytesIO(img_data))
            # 创建一个带有透明背景的RGBA图像
            gif_image = Image.new('RGBA', png_image.size, (0, 0, 0, 0))

            # 将PNG图像粘贴到GIF图像上
            gif_image.paste(png_image, (0, 0), png_image)

            # 将GIF图像保存到文件
            gif_image.save(file_path, format='GIF', transparency=0)

            # print(file_path)
            await catch_str.finish(MessageSegment.image(file=Path(file_path)))
        else:
            await catch_str.finish(MessageSegment.image(file=img_data))
    except FinishedException as e:
        pass
    except Exception as e:
        nonebot.logger.info(e)
        msg = '果咩，发送图片失败喵，可能图片被ban了'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


help = on_command("自定义去背景帮助", aliases={"自定义去背景help"})

@help.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = "命令如下(命令前缀自行添加)：\n" +\
        "自定义去背景 -img <IMAGE>" +\
        " [-s --size -最大输出分辨率 <最大输出图像分辨率 'preview/full/auto'>]" +\
        " [-t --type -前景类型 <前景类型 'auto/person/product/car'>]" +\
        " [-tl --type_level -前景类型级别 <检测到的前景类型的分类级别 'none/1/2/latest'>]\n" +\
        " [-r --roi -感兴趣区域 <感兴趣区域 x1 y1 x2 y2，如'0% 0% 100% 100%'>]" +\
        " [-c --crop -裁剪空白区 <是否裁剪掉所有空白区域 'true/false'>]" +\
        " [-p --position -定位主题 <在图像画布中定位主题 'center/original/从“0%”到“100%”的一个值(水平和垂直)或两个值(水平、垂直)'>]\n" +\
        " [-sc --scale -缩放主体 <相对于图像总尺寸缩放主体 从“10%”到“100%”之间的任何值，也可以是“original”(默认)。缩放主体意味着“位置=中心”(除非另有说明)。>]" +\
        " [-ad --add_shadow -人工阴影 <是否向结果添加人工阴影 'true/false'>]" +\
        " [-se --semitransparency -半透明区域 <结果中是否包含半透明区域 'true/false'>]\n" +\
        "\n命令起始：自定义去背景 或 remove_bg \n" +\
        "-img 必选参数，后面追加<IMAGE>图片（回复的话，图片就不用了）\n" +\
        "-s 可选参数 -s可以改成 --size 或 -最大输出分辨率，含义是最大输出图像分辨率，传参内容是'preview/full/auto'（3选1）\n" +\
        "其他的[]都是可选参数，含义和-s相同，不再赘述。" +\
        "\n例如：\n/自定义去背景 -img <IMAGE> -s 'preview'\n" +\
        "/remove_bg -img <IMAGE> -s 'full' -r '30% 30% 60% 60%' -ad 'true'\n"
    await catch_str.finish(Message(f'{msg}'), at_sender=True)


remove_bg_parser = ArgumentParser()
remove_bg_parser.add_argument("-s", "--size", "-最大输出分辨率", required=False,
                           type=str, default="auto", nargs="*", help="最大输出图像分辨率 'preview/full/auto'", dest="size")
remove_bg_parser.add_argument("-t", "--type", "-前景类型", required=False,
                           type=str, default="auto", help="前景类型 'auto/person/product/car'", dest="type")
remove_bg_parser.add_argument("-tl", "--type_level", "-前景类型级别", required=False,
                           type=str, default="1", nargs="*", help="检测到的前景类型的分类级别 'none/1/2/latest'", dest="type_level")
remove_bg_parser.add_argument("-r", "--roi", "-感兴趣区域", required=False,
                           type=str, default="0% 0% 100% 100%", nargs="*", help="感兴趣区域 x1 y1 x2 y2，如'0% 0% 100% 100%'", dest="roi")
remove_bg_parser.add_argument("-c", "--crop", "-裁剪空白区", required=False,
                           type=str, default="false", help="是否裁剪掉所有空白区域", dest="crop")
remove_bg_parser.add_argument("-p", "--position", "-定位主题", required=False,
                           type=str, default="original", nargs="*", help="在图像画布中定位主题 'center/original/从“0%”到“100%”的一个值(水平和垂直)或两个值(水平、垂直)'", dest="position")
remove_bg_parser.add_argument("-sc", "--scale", "-缩放主体", required=False,
                           type=str, default="original", nargs="*", help="相对于图像总尺寸缩放主体 从“10%”到“100%”之间的任何值，也可以是“original”(默认)。缩放主体意味着“位置=中心”(除非另有说明)。", dest="scale")
remove_bg_parser.add_argument("-ad", "--add_shadow", "-人工阴影", required=False,
                           type=str, default="false", help="是否向结果添加人工阴影", dest="add_shadow")
remove_bg_parser.add_argument("-se", "--semitransparency", "-半透明区域", required=False,
                           type=str, default="true", nargs="*", help="结果中是否包含半透明区域", dest="semitransparency")
remove_bg_parser.add_argument("-img", "--image", "-图片",
                           type=str, default="", nargs="*", help="后面传入待处理的图片", dest="image")


catch_str2 = on_shell_command(
    "remove_bg",
    aliases={"自定义去背景"},
    parser=remove_bg_parser,
    priority=5
)

@catch_str2.handle()
async def _(bot: Bot, event: MessageEvent, args: Namespace = ShellCommandArgs()):
    # 信息源自 群聊或私聊
    msg_from = "group"
    # 判断消息类型
    if not isinstance(event, GroupMessageEvent):
        msg_from = "private"
    
    url = ""

    reply = event.reply
    if reply:
        for seg in reply.message['image']:
            url = seg.data["url"]
    for seg in event.message['image']:
        url = seg.data["url"]
    if url:
        nonebot.logger.info(url)
        # 由于私聊的图片链接直接传给trace无法获取正确的图片，所以本地做了处理
        if msg_from == "group":
            img_data = await remove_by_url(url, args)
        else:
            img_data = await remove_by_img(url, args)

        if img_data == None:
            msg = '请求出错，可能是网络问题或者API寄了喵~'
            await catch_str2.finish(Message(f'{msg}'), at_sender=True)
        
        # nonebot.logger.info(img_data)

        try:
            if msg_from == "group":
                dir_path = Path(__file__).parent
                file_path = dir_path / (await get_current_timestamp_seconds() + '.gif')
                file_path = str(file_path)
                
                png_image = Image.open(io.BytesIO(img_data))
                # 创建一个带有透明背景的RGBA图像
                gif_image = Image.new('RGBA', png_image.size, (0, 0, 0, 0))

                # 将PNG图像粘贴到GIF图像上
                gif_image.paste(png_image, (0, 0), png_image)

                # 将GIF图像保存到文件
                gif_image.save(file_path, format='GIF', transparency=0)

                # print(file_path)
                await catch_str2.finish(MessageSegment.image(file=Path(file_path)))
            else:
                await catch_str2.finish(MessageSegment.image(file=img_data))
        except FinishedException as e:
            pass
        except Exception as e:
            nonebot.logger.info(e)
            msg = '果咩，发送图片失败喵，可能图片被ban了'
            await catch_str2.finish(Message(f'{msg}'), at_sender=True)
    else:
        await catch_str2.finish("请回复图片或在命令结尾追加图片喵~命令结束")



async def remove_by_url(url, args=None):
    # nonebot.logger.info(args)
    data_json = await args_to_json(url, args)
    nonebot.logger.debug(data_json)
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.remove.bg/v1.0/removebg",
            data=data_json,
            headers={
                "X-Api-Key": remove_bg_api_key
            }
        ) as resp:
            nonebot.logger.debug(resp)
            if resp.status == 200:
                return await resp.read()
            else:
                return None


async def remove_by_img(url, args):
    # nonebot.logger.info(args)
    data_json = await args_to_json(url, args)
    nonebot.logger.debug(data_json)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.content.read()
            data_json["image_url"] = ""
            data_json["image_file"] = content
            nonebot.logger.debug(data_json)
            async with aiohttp.ClientSession() as session2:
                async with session2.post(
                    "https://api.remove.bg/v1.0/removebg",
                    data=data_json,
                    headers={
                        "X-Api-Key": remove_bg_api_key
                    }
                ) as resp2:
                    nonebot.logger.debug(resp2)
                    if resp2.status == 200:
                        return await resp2.read()
                    else:
                        return None


async def args_to_json(url, args):
    if args:
        nonebot.logger.info(args)
        data_json = {
            "size": args.size if isinstance(args.size, str) else args.size[0], # 最大输出图像分辨率 preview/full/auto
            "type": args.type if isinstance(args.type, str) else args.type[0], # 前景类型 auto/person/product/car
            "type_level": args.type_level if isinstance(args.type_level, str) else args.type_level[0], # 检测到的前景类型的分类级别 none/1/2/latest
            "format": "png", # 结果图像格式 auto/png/jpg/zip
            "roi": args.roi if isinstance(args.roi, str) else args.roi[0], # 感兴趣区域 x1 y1 x2 y2
            "crop": args.crop if isinstance(args.crop, str) else args.crop[0], # 是否裁剪掉所有空白区域
            "position": args.position if isinstance(args.position, str) else args.position[0], # 在图像画布中定位主题 center/original/从“0%”到“100%”的一个值(水平和垂直)或两个值(水平、垂直)
            "scale": args.scale if isinstance(args.scale, str) else args.scale[0], # 相对于图像总尺寸缩放主体 从“10%”到“100%”之间的任何值，也可以是“original”(默认)。缩放主体意味着“位置=中心”(除非另有说明)。
            "add_shadow": args.add_shadow if isinstance(args.add_shadow, str) else args.add_shadow[0], # 是否向结果添加人工阴影
            "semitransparency": args.semitransparency if isinstance(args.semitransparency, str) else args.semitransparency[0], # 结果中是否包含半透明区域
            "image_url": url,
            "image_file": ""
        }
    else:
        data_json = {
            "size": "auto", # 最大输出图像分辨率 preview/full/auto
            "type": "auto", # 前景类型 auto/person/product/car
            "type_level": "1", # 检测到的前景类型的分类级别 none/1/2/latest
            "format": "png", # 结果图像格式 auto/png/jpg/zip
            "roi": "0% 0% 100% 100%", # 感兴趣区域 x1 y1 x2 y2
            "crop": "false", # 是否裁剪掉所有空白区域
            "position": "original", # 在图像画布中定位主题 center/original/从“0%”到“100%”的一个值(水平和垂直)或两个值(水平、垂直)
            "scale": "original", # 相对于图像总尺寸缩放主体 从“10%”到“100%”之间的任何值，也可以是“original”(默认)。缩放主体意味着“位置=中心”(除非另有说明)。
            "add_shadow": "false", # 是否向结果添加人工阴影
            "semitransparency": "true", # 结果中是否包含半透明区域
            "image_url": url, # 后面传入待处理的图片
            "image_file": ""
        }
    return data_json


# 获取时间戳的当前的秒
async def get_current_timestamp_seconds():
    current_timestamp = int(time.time())
    return str(current_timestamp % 60)

