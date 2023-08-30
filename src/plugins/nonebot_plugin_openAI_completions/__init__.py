import nonebot
# import aiohttp
import openai
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


openai_api_key = ''
openai_api_base = 'https://api.openai.com/v1'
openai_model = 'gpt-3.5-turbo'
openai_max_tokens = 16
openai_temperature = 1


# 获取env配置
try:
    nonebot.logger.debug(f"openai_api_key={nonebot.get_driver().config.openai_api_key}")
    openai_api_key = nonebot.get_driver().config.openai_api_key
    nonebot.logger.debug(f"openai_api_base={nonebot.get_driver().config.openai_api_base}")
    openai_api_base = nonebot.get_driver().config.openai_api_base
    nonebot.logger.debug(f"openai_model={nonebot.get_driver().config.openai_model}")
    openai_model = nonebot.get_driver().config.openai_model
    nonebot.logger.debug(f"openai_max_tokens={nonebot.get_driver().config.openai_max_tokens}")
    openai_max_tokens = nonebot.get_driver().config.openai_max_tokens
    nonebot.logger.debug(f"openai_temperature={nonebot.get_driver().config.openai_temperature}")
    openai_temperature = nonebot.get_driver().config.openai_temperature
except:
    nonebot.logger.warning("openai部分配置没有配置，采用默认配置喵~。")

openai.api_key = openai_api_key
openai.api_base = openai_api_base

catch_str = on_command("cplt", aliases={"openai", "gpt"})


@catch_str.handle()
async def _(bot: Bot, event: Event, state: T_State):
    content = event.get_plaintext().strip()
    # nonebot.logger.info(content)

    msg = await chatgpt_response(content) 
    await catch_str.finish(Message(f'{msg}'), at_sender=True)


# 将输入的文本作为 prompt 进行请求
async def chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model=openai_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=openai_max_tokens,
            temperature=openai_temperature
        )

        nonebot.logger.info(response)
        return response.choices[0].message["content"]
    except Exception as e:
        nonebot.logger.error(e)
        return str(e)
