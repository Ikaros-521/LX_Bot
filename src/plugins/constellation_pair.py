import aiohttp, json
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg


catch_str = on_command('星座配对', aliases={"星座相性"})


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    data_json = await get_data(content)
    try:
        msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_data(content):
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/543
    api_key = ""
    men = ""
    women = ""
    # 解析2个传参
    if content[0] == ' ':
        content = content[1:]
        men = content.split()[0]
        women = content.split()[1]
    else:
        men = content.split()[0]
        women = content.split()[1]

    API_URL = 'http://apis.juhe.cn/xzpd/query?men=' + men + '&women=' + women + '&key=' + api_key
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret
