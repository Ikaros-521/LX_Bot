import aiohttp, json
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg


# 这是一套on_command的模板 命令后的内容通通传入，调用的接口返回的json，转字符串后打印
cmd1 = on_command('权重')
@cmd1.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    API_URL = 'http://tfapi.top/API/qqqz.php?type=json&qq=' + content
    data_json = await get_data_json(API_URL)

    msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)

    await cmd1.finish(Message(f'{msg}'), at_sender=True)


# 这是一套on_command的模板 命令后的内容通通传入，调用的接口返回的字符串直接打印
cmd2 = on_command('随机sfz')
@cmd2.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    API_URL = 'http://tfapi.top/API/sjsfz.php'
    data_text = await get_data_text(API_URL)

    msg = '\n' + data_text

    await cmd2.finish(Message(f'{msg}'), at_sender=True)


cmd3 = on_command('随机网易小号')
@cmd3.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    API_URL = 'http://tfapi.top/API/wyzh.php'
    data_text = await get_data_text(API_URL)

    msg = '\n' + data_text

    await cmd3.finish(Message(f'{msg}'), at_sender=True)


cmd4 = on_command('随机yh')
@cmd4.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    API_URL = 'http://tfapi.top/API/yht.php?return=txt'
    data_text = await get_data_text(API_URL)

    msg = '\n' + data_text

    await cmd4.finish(Message(f'{msg}'), at_sender=True)


cmd5 = on_command('语录')
@cmd5.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    # 传参校验
    if content not in ["动漫","恋爱","鼓励","孤独","搞笑","友情","歌词"]:
        msg = '\n传参仅支持：动漫、恋爱、鼓励、孤独、搞笑、友情、歌词。例如：/语录 动漫'
        await cmd5.finish(Message(f'{msg}'), at_sender=True)

    API_URL = 'http://tfapi.top/API/yulu.php?type=' + content
    data_text = await get_data_text(API_URL)

    msg = '\n' + data_text

    await cmd5.finish(Message(f'{msg}'), at_sender=True)


# 传入拼接好的get请求链接 和 请求头(可以不传），返回json
async def get_data_json(API_URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret


# 传入拼接好的get请求链接 和 请求头(可以不传），返回字符串
async def get_data_text(API_URL, header={}):
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get(url=API_URL, headers=header) as response:
            ret = await response.read()
    # nonebot.logger.info(ret)
    return ret.decode('utf-8')