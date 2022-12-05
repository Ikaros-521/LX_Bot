import nonebot
import aiohttp
from nonebot import on_command, on_message, on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import (
    Bot, 
    Event,
    GroupMessageEvent,
    Message,
    MessageSegment,
    MessageEvent,
    PrivateMessageEvent,
)


api_url = 'https://api.openai.com/v1/completions'

# 使用 openai 的 secret_key 进行身份验证
secret_key = ''

# 获取env配置
try:
    nonebot.logger.debug(nonebot.get_driver().config.openai_secret_key)
    secret_key = nonebot.get_driver().config.openai_secret_key
except:
    secret_key = ""
    nonebot.logger.warning("openai_secret_key没有配置，功能无法使用喵~。")


catch_str = on_command("cplt", aliases={"openai", "ai"})


@catch_str.handle()
async def _(bot: Bot, event: Event, state: T_State):
    content = event.get_plaintext().strip()
    # nonebot.logger.info(content)

    msg = await chatgpt_response(content) 
    await catch_str.finish(Message(f'{msg}'), at_sender=True)


# 将输入的文本作为 prompt 进行请求
async def chatgpt_response(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {secret_key}'
    }
    data = """
    {
        "prompt": "%s",
        "model": "text-davinci-002",
        "max_tokens": 64,
        "temperature": 0.5,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    """ % prompt
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, data=data) as response:
            response_text = await response.json()
            nonebot.logger.info(response_text)
            return response_text['choices'][0]['text']
