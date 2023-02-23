import nonebot
import aiohttp, asyncio, time
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import (
    Bot, 
    Event,
    GroupMessageEvent,
    Message,
    MessageSegment,
    MessageEvent,
    # PrivateMessageEvent,
)
from nonebot.params import CommandArg, ShellCommandArgv
# from nonebot.rule import ArgumentParser, ParserExit
from nonebot.plugin import PluginMetadata


help_text = f"""
命令如下：
1、先发送命令，再发送图片（命令前缀请自行替换）
先发送`/图片来源`或`/trace`或`/图片定位`，等bot返回`请发送需要识别的图片喵~`后，发送需要识别的图片即可。  

2、命令+图片
编辑消息`/图片来源[待识别的图片]`或`/trace[待识别的图片]`或`/图片定位[待识别的图片]`发送即可。  

3、回复图片+命令
回复需要处理的图片，发送`/图片来源`或`/trace`或`/图片定位`即可。
""".strip()

__plugin_meta__ = PluginMetadata(
    name = '动画截图场景追溯',
    description = '调用trace.moe的API查询动画截图源自的作品名和时间段',
    usage = help_text
)

# 自动撤回时间 默认0秒 不撤回
trace_moe_withdraw_time = 0
# 最大返回查询结果数
trace_moe_max_ret = 3
# 转发消息源自的QQ 随便了
superuser = 123

# 获取env配置
try:
    nonebot.logger.debug(nonebot.get_driver().config.trace_moe_withdraw_time)
    trace_moe_withdraw_time = nonebot.get_driver().config.trace_moe_withdraw_time
except AttributeError as e:
    nonebot.logger.info("trace_moe_withdraw_time没有配置，默认为0，不撤回")

try:
    nonebot.logger.debug(nonebot.get_driver().config.trace_moe_max_ret)
    trace_moe_max_ret = nonebot.get_driver().config.trace_moe_max_ret
except AttributeError as e:
    nonebot.logger.warning("trace_moe_max_ret没有配置，默认为3")

catch_str = on_command("图片来源", aliases={"trace", "图片定位"})
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


@catch_str.got("src_img", prompt="请发送需要识别的图片喵~")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    # 信息源自 群聊或私聊
    msg_from = "group"
    # 判断消息类型
    msg = event.get_plaintext()
    if isinstance(event, GroupMessageEvent):
        # nonebot.logger.info("群聊")
        group = str(event.group_id)
    else:
        # nonebot.logger.info("私聊")
        private = event.get_user_id()
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

    # 由于私聊的图片链接直接传给trace无法获取正确的图片，所以本地做了处理
    if msg_from == "group":
        info_json = await search_by_url(url)
    else:
        info_json = await search_by_img(url)

    # 为后面撤回消息做准备
    msg_ids = []

    try:
        # 判断返回代码
        if info_json['error'] != "":
            msg = info_json['error']
            await catch_str.finish(Message(f'{msg}'), at_sender=True)
        else:
            try:
                # nonebot.logger.info(info_json)
                msgList = []
                for i in range(len(info_json['result'])):
                    # 最大返回数
                    if i >= int(trace_moe_max_ret):
                        break
                    out_str = ""
                    out_str += str(i + 1) + "."
                    out_str += "\n作品名：" + info_json["result"][i]["filename"]
                    out_str += "\n相似度：" + str(round(info_json["result"][i]["similarity"], 2))
                    out_str += "\n时间段：" + await time_change(info_json["result"][i]["from"]) + " - " + await time_change(info_json["result"][i]["to"])
                    out_str += "\n参考图如下\n"

                    msgList.extend(
                        [
                            MessageSegment.node_custom(
                                user_id=superuser,
                                nickname="bot",
                                content=Message(MessageSegment.text(out_str)),
                            ),
                            MessageSegment.node_custom(
                                user_id=superuser,
                                nickname="bot",
                                content=Message(MessageSegment.image(file=info_json["result"][i]["image"], timeout=10)),
                            ),
                        ]
                    )
            except (KeyError, TypeError, IndexError) as e:
                msg = '果咩，result解析失败喵~接口可能返回错误或源码bug喵\n' + str(e)
                await catch_str.finish(Message(f'{msg}'), at_sender=True)    

            # 记录开始发送的时间
            start_time = time.time()  

            try:
                # 判断消息类型
                if msg_from == "group":
                    msg_ids.append((await bot.send_group_forward_msg(group_id=group, messages=msgList))['message_id'])
                else:
                    msg_ids.append((await bot.send_private_forward_msg(user_id=private, messages=msgList))['message_id'])
            except:
                msg = '果咩，数据发送失败喵~请查看源码和日志定位问题原因'
                await catch_str.finish(Message(f'{msg}'), at_sender=True)

            # 自动撤回涩图
            if trace_moe_withdraw_time != 0:
                try:
                    timeLeft = trace_moe_withdraw_time + start_time - time.time()  # 计算从开始发送到目前仍剩余的保留时间
                    await asyncio.sleep(1 if timeLeft <= 0 else timeLeft)
                    for msg_id in msg_ids:
                        await bot.delete_msg(message_id=msg_id)
                except:
                    pass
    except (KeyError, TypeError, IndexError) as e:
        msg = '果咩，查询失败喵~接口可能挂了喵。\n' + str(e)
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


# 调用trace.moe API Search by image URL
async def search_by_url(url):
    API_URL = 'https://api.trace.moe/search?url=' + url
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            ret = await response.json()
    # nonebot.logger.info(ret)
    return ret


# 调用trace.moe API Search by image upload
async def search_by_img(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.content.read()
            API_URL = 'https://api.trace.moe/search'
            async with aiohttp.ClientSession() as session2:
                async with session2.post(url=API_URL, data=content, headers={"Content-Type": "image/jpeg"}) as response:
                    ret = await response.json()
            # nonebot.logger.info(ret)
            return ret


# 时间转换
async def time_change(srt_time):
    hour = int(srt_time / 3600)
    min = int(int(srt_time) % 3600 / 60)
    sec = int(srt_time) % 60

    if hour > 0:
        hour = str(hour) if hour >= 10 else "0" + str(hour)
    else:
        hour = "00"
    if min > 0:
        min = str(min) if min >= 10 else "0" + str(min)
    else:
        min = "00"
    if sec > 0:
        sec = str(sec) if sec >= 10 else "0" + str(sec)
    else:
        sec = "00"
    
    # nonebot.logger.info(hour + ":" + min + ":" + sec)
    return hour + ":" + min + ":" + sec  # 01:09:46 时分秒