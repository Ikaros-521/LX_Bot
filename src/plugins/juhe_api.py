import aiohttp, json
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

help_text = f"""
命令如下：
暂时懒得写
""".strip()

__plugin_meta__ = PluginMetadata(
    name = '聚合API相关插件',
    description = '调用聚合API',
    usage = help_text
)

catch_str1 = on_command('鸡汤', aliases={"正能量"})
catch_str2 = on_command('星座配对', aliases={"星座相性"})
catch_str3 = on_command('成语')
catch_str4 = on_command('查手机', aliases={"查手机号", "手机号"})
catch_str5 = on_command('生肖配对', aliases={"生肖相性"})
catch_str6 = on_command('解梦', aliases={"周公解梦"})
catch_str7 = on_command('字典', aliases={"新华字典"})
catch_str8 = on_command('笑话')

# 此处填写api_key，对应catch的下标
api_key = [
    "填写自己的api_key，下标0做为提示使用（其实是为了对齐",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]

@catch_str1.handle()
async def send_msg(bot: Bot, event: Event):
    # 鸡汤 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/669
    url = 'https://apis.juhe.cn/fapig/soup/query?key=' + api_key[1]
    data_json = await common_get_return_json(url)
    try:
        msg = '\n' + str(data_json["result"]["text"])
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str1.finish(Message(f'{msg}'), at_sender=True)


@catch_str2.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    # 星座配对 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/543
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

    url = 'http://apis.juhe.cn/xzpd/query?men=' + men + '&women=' + women + '&key=' + api_key[2]
    
    data_json = await common_get_return_json(url)
    try:
        msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str2.finish(Message(f'{msg}'), at_sender=True)


@catch_str3.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    # 成语 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/157
    url = 'http://apis.juhe.cn/idioms/query?wd=' + content + '&key=' + api_key[3]

    data_json = await common_get_return_json(url)

    msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)

    await catch_str3.finish(Message(f'{msg}'), at_sender=True)


@catch_str4.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/11
    url = 'http://apis.juhe.cn/mobile/get?phone=' + content + '&key=' + api_key[4]

    data_json = await common_get_return_json(url)
    try:
        msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str4.finish(Message(f'{msg}'), at_sender=True)


@catch_str5.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/539
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

    url = 'http://apis.juhe.cn/sxpd/query?men=' + men + '&women=' + women + '&key=' + api_key[5]
    
    data_json = await common_get_return_json(url)
    try:
        msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str5.finish(Message(f'{msg}'), at_sender=True)


@catch_str6.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/156
    url = 'http://v.juhe.cn/dream/query?full=1&q=' + content + '&key=' + api_key[6]

    data_json = await common_get_return_json(url)
    try:
        msg = '\n' + json.dumps(data_json, indent=2, ensure_ascii=False)
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str6.finish(Message(f'{msg}'), at_sender=True)


@catch_str7.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/156
    url = 'http://v.juhe.cn/xhzd/query?word=' + content + '&key=' + api_key[7]
    data_json = await common_get_return_json(url)
    try:
        msg = '\n' + str(data_json["result"]["jijie"])
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str7.finish(Message(f'{msg}'), at_sender=True)


@catch_str8.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    # 填写自己的api_key 获取地址：https://www.juhe.cn/docs/api/id/95
    url = 'http://v.juhe.cn/joke/randJoke.php?key=' + api_key[8]
    data_json = await common_get_return_json(url)
    try:
        msg = '\n' + data_json["result"][0]["content"]
    except:
        msg = '数据解析失败，额度用完或接口寄了喵~'

    await catch_str8.finish(Message(f'{msg}'), at_sender=True)


# 通用get请求返回json
async def common_get_return_json(url, timeout=60):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, timeout=timeout) as response:
                result = await response.read()
                ret = json.loads(result)
    except:
        return None
    # nonebot.logger.info(ret)
    return ret
