from nonebot.adapters.onebot.v11 import Message
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg
from nonebot.exception import FinishedException
from nonebot.log import logger

import json
# import html

# 注意：不兼容包含实体编码的字符串 例如：&lt; 这种会被转换为 <
cmd1 = on_command('json压缩', aliases={"JSON压缩"})
cmd2 = on_command('json格式化', aliases={"JSON格式化"})


@cmd1.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    # 将接受一个包含实体编码的字符串，然后返回一个字符串，其中所有实体编码都被替换为它们对应的字符。
    # decoded_content = html.unescape(content)
    decoded_content = content.replace("&#91;", "[").replace("&#93;", "]")
    logger.info(decoded_content)

    try:
        # 将JSON字符串转换为Python对象
        data = json.loads(decoded_content)
        data_str = '\n' + json.dumps(data, indent=None, ensure_ascii=False)
        await cmd2.finish(Message(f'{data_str}'), at_sender=True)
    except FinishedException:
        pass
    except Exception as e:
        await cmd1.finish(Message('压缩失败，请检查输入的json串格式是否正确~'), at_sender=True)


@cmd2.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    # decoded_content = html.unescape(content)
    decoded_content = content.replace("&#91;", "[").replace("&#93;", "]")
    logger.info(decoded_content)

    try:
        # 将JSON字符串转换为Python对象
        data = json.loads(decoded_content)
        data_str = '\n' + json.dumps(data, indent=4, ensure_ascii=False)
        await cmd2.finish(Message(f'{data_str}'), at_sender=True)
    except FinishedException:
        pass
    except Exception as e:
        await cmd2.finish(Message('格式化失败，请检查输入的json串格式是否正确~'), at_sender=True)


