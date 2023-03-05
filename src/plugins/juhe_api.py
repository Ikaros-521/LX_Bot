import aiohttp, json
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg


catch_str1 = on_command('鸡汤', aliases={"正能量"})
catch_str2 = on_command('星座配对', aliases={"星座相性"})
catch_str3 = on_command('成语')
catch_str4 = on_command('查手机', aliases={"查手机号", "手机号"})
catch_str5 = on_command('生肖配对', aliases={"生肖相性"})
catch_str6 = on_command('解梦', aliases={"周公解梦"})
catch_str7 = on_command('字典', aliases={"新华字典"})
catch_str8 = on_command('笑话')


@catch_str1.handle()
async def send_msg(bot: Bot, event: Event):
    data_json = await get_data()
    try:
        msg = '\n' + str(data_json["result"]["text"])
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str1.finish(Message(f'{msg}'), at_sender=True)


async def get_data():
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/669
    api_key = ""
    API_URL = 'https://apis.juhe.cn/fapig/soup/query?key=' + api_key
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret


@catch_str2.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    data_json = await get_data2(content)
    try:
        msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str2.finish(Message(f'{msg}'), at_sender=True)


async def get_data2(content):
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


@catch_str3.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    data_json = await get_data3(content)

    msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)

    await catch_str3.finish(Message(f'{msg}'), at_sender=True)


async def get_data3(content):
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/157
    api_key = ""
    API_URL = 'http://apis.juhe.cn/idioms/query?wd=' + content + '&key=' + api_key
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret


@catch_str4.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    data_json = await get_data4(content)
    try:
        msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str4.finish(Message(f'{msg}'), at_sender=True)


async def get_data4(content):
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/11
    api_key = ""
    API_URL = 'http://apis.juhe.cn/mobile/get?phone=' + content + '&key=' + api_key
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret


@catch_str5.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    data_json = await get_data5(content)
    try:
        msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str5.finish(Message(f'{msg}'), at_sender=True)


async def get_data5(content):
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/539
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

    API_URL = 'http://apis.juhe.cn/sxpd/query?men=' + men + '&women=' + women + '&key=' + api_key
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret


@catch_str6.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    data_json = await get_data6(content)
    try:
        msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str6.finish(Message(f'{msg}'), at_sender=True)


async def get_data6(content):
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/156
    api_key = ""
    API_URL = 'http://v.juhe.cn/dream/query?full=1&q=' + content + '&key=' + api_key
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret


@catch_str7.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    data_json = await get_data7(content)
    try:
        msg = '\n' + str(data_json["result"]["jijie"])
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str7.finish(Message(f'{msg}'), at_sender=True)


async def get_data7(content):
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/156
    api_key = ""
    API_URL = 'http://v.juhe.cn/xhzd/query?word=' + content + '&key=' + api_key
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret


@catch_str8.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    data_json = await get_data8()
    try:
        msg = '\n' + data_json["result"][0]["content"]
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str8.finish(Message(f'{msg}'), at_sender=True)


async def get_data8():
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/95
    api_key = ""
    API_URL = 'http://v.juhe.cn/joke/randJoke.php?key=' + api_key
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret
