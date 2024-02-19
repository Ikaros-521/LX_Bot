import json, re
import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event
# import nonebot

catch_str = on_command('新视频搜索')

header1 = {
    'content-type': 'text/plain; charset=utf-8',
    'cookie': "",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
}


@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    # print(content)

    # 以空格分割 关键词 条数
    content = content.split()
    keyword = ""
    page_size = "1"

    if len(content) == 1:
        keyword = content[0]
    elif len(content) > 1:
        keyword = content[0]
        page_size = str(int(content[1]))
    else:
        msg = '传参错误，命令格式【/新视频搜索 关键词 条数】'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    info_json = await get_info(keyword, page_size)
    # nonebot.logger.info(info_json)

    try:
        result = info_json['data']['result']
    except KeyError:
        msg = '\n查询失败，单次查询数最大为50'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    msg = "\n 查询内容：" + keyword + "\n" + \
          " 显示格式为：标题 | up | 链接 \n"
    for i in range(len(result)):
        msg += " 【" + re.sub(r'<[^>]+>', '', (str(result[i]["title"])) + " | " + result[i]["author"] + " | " + str(result[i]["arcurl"]) + ' 】\n'
    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_info(keyword, page_size):
    API_URL = f'https://api.bilibili.com/x/web-interface/wbi/search/type?search_type=video&page=1&page_size={page_size}&keyword={keyword}'

    async with aiohttp.ClientSession(headers=header1) as session:
        async with session.get(url=API_URL, headers=header1) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret
