# 安装相关依赖库（别告诉我你没装nb
# pip install aiohttp （发送HTTP请求用）
import json
import aiohttp
import random
import os
from pathlib import Path

from urllib.parse import urljoin
import traceback

import nonebot
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.exception import FinishedException


cmd7 = on_command('知识库')

@cmd7.handle()
async def _(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        # 发送get请求，调用API获取返回的文本赋值给msg，接口是统计字数的
        msg = await get_anythingllm_resp(content)

        # 返回的data_json如果是None的话 就是请求中出问题了
        if None == msg:
            msg = "\n请求异常，可能是网络问题或者API挂了喵~（请检查后台日志排查）"
        # 设置 reply_message 参数为 True，表示回复原来的消息
        await cmd7.finish(Message(f'{msg}'), reply_message=True)
    # FinishedException，指示 NoneBot 结束当前 Handler 且后续 Handler 不再被运行。可用于结束用户会话。
    except FinishedException:
        pass
    except Exception as e:
        # 打印下异常报错
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await cmd7.finish(Message(f'{msg}'), reply_message=True)

# 异步 get请求API，API返回一个文本格式的数据，不需要解析，直接utf8解码返回
async def get_anythingllm_resp(prompt):
    try:
        api_ip_port = 'http://45.77.162.143:56789'
        workspace_slug = 'ai-vtb'
        mode = 'chat'
        api_key = 'S1PPG9B-YP2M8NX-Q64ZBF1-Y4K5DCS'

        url = urljoin(api_ip_port, f"/api/v1/workspace/{workspace_slug}/chat")

        data_json = {
            "message": prompt,
            "mode": mode
        }

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=data_json, headers=headers) as response:
                response.raise_for_status()  # 检查响应的状态码
                result = await response.json()

                nonebot.logger.debug(result)

                if "textResponse" in result:
                    return result["textResponse"]

                nonebot.logger.error(f"AnythingLLM 对话失败: {result['message']}")
                return None
    except Exception:
        nonebot.logger.error(traceback.format_exc())
        return None
    
