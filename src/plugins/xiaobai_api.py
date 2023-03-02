import nonebot
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.params import CommandArg
import aiohttp, json


from nonebot.plugin import PluginMetadata


help_text = f"""
插件命令(太多了，暂时不写）：
/温柔语录
/微甜语录
/超强语录 传入语录id（不传id可以获取id列表）

/域名查ip 传入域名
/域名查IP 传入域名

/放假

/老黄历

/扒站 传入url

/邮编查询 传入地名
/邮编 传入地名

/缘分 小白 小红
/缘分测试 黑 白

/qq估值 传入QQ号

/垃圾分类 传入垃圾名
/什么垃圾 传入垃圾名

/文本倒序 需要倒序的文本
/倒序 需要倒序的文本

/淘宝联想词 传入商品名关键词
/百度联想词 传入关键词

/转emoji 传入你想要转成emoji的文字
/转emj 传入你想要转成emoji的文字

/url编码 传入内容
/URL编码 传入内容
/url解码 传入内容
/URL解码 传入内容

/字数 传入需要判断字数的文本

""".strip()

__plugin_meta__ = PluginMetadata(
    name = '小白API相关功能',
    description = '适用于nonebot2 v11的小白API相关功能',
    usage = help_text
)


# 所有的命令都在这哦，要改命令触发关键词的请自便
catch_str = on_command("温柔语录")
catch_str2 = on_command("微甜语录")
catch_str3 = on_command("超强语录", aliases={"超级语录"})

catch_str4 = on_command("域名查IP", aliases={"域名查ip"})

catch_str5 = on_command("放假")

catch_str6 = on_command("老黄历")

catch_str7 = on_command("扒站")

catch_str8 = on_command("邮编查询", aliases={"邮编"})

catch_str9 = on_command("缘分", aliases={"缘分测试"})

catch_str10 = on_command("qq估值", aliases={"QQ估值"})

catch_str11 = on_command("垃圾分类", aliases={"什么垃圾"})

catch_str12 = on_command("文本倒序", aliases={"倒序"})

catch_str13 = on_command("淘宝联想词")
catch_str14 = on_command("百度联想词")

catch_str15 = on_command("转emoji", aliases={"转emj"})

catch_str16 = on_command("url编码", aliases={"URL编码"})
catch_str17 = on_command("url解码", aliases={"URL解码"})

catch_str18 = on_command("字数")

# 
@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    try:
        msg = await get_quotation(0)

        await catch_str.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


@catch_str2.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    try:
        msg = await get_quotation(1)

        await catch_str2.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str2.finish(Message(f'{msg}'), at_sender=True)


@catch_str3.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    content = content.split()

    id = 1

    try:
        if len(content) == 0:
            msg = '\n语录id：\n' + await get_super_quotation(0)
            await catch_str3.finish(Message(f'{msg}'), at_sender=True)
        else:
            id = int(content[0])

            msg = await get_super_quotation(id)
            await catch_str3.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str3.finish(Message(f'{msg}'), at_sender=True)


async def get_quotation(type):
    try:
        if type == 0:
            API_URL = 'http://ovooa.com/API/wryl/api.php'
        elif type == 1:
            API_URL = 'https://xiaobai.klizi.cn/API/other/wtqh.php'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')


async def get_super_quotation(id):
    try:
        if id == 0:
            API_URL = 'https://xiaobai.klizi.cn/API/other/cqyl.php?data=&id='
        else:
            API_URL = 'https://xiaobai.klizi.cn/API/other/cqyl.php?data=&id=' + str(id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')


@catch_str4.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        data_json = await get_data4(content)
        msg = json.dumps(data_json, indent=2, ensure_ascii=False)
        await catch_str4.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str4.finish(Message(f'{msg}'), at_sender=True)


async def get_data4(content):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/wl/ip_address.php?data=&url=' + content
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                result = await response.read()
                ret = json.loads(result)
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret


@catch_str5.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    try:
        data_json = await get_data5()

        msg = data_json['tts']
        await catch_str5.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str5.finish(Message(f'{msg}'), at_sender=True)


async def get_data5():
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/holiday.php'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                result = await response.read()
                ret = json.loads(result)
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret


@catch_str6.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    try:
        msg = await get_data6()
        await catch_str6.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str6.finish(Message(f'{msg}'), at_sender=True)


async def get_data6():
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/laohuangli.php'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')


@catch_str7.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        data_json = await get_data7(content)
        msg = json.dumps(data_json, indent=2, ensure_ascii=False)
        await catch_str7.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str7.finish(Message(f'{msg}'), at_sender=True)


async def get_data7(content):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/wl/bz.php?url=' + content
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                result = await response.read()
                ret = json.loads(result)
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret


@catch_str8.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        msg = await get_data8(content)
        await catch_str8.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str8.finish(Message(f'{msg}'), at_sender=True)


async def get_data8(content):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/yzbm.php?msg=' + content
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')


@catch_str9.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    content = content.split()

    name1 = ""
    name2 = ""

    if len(content) > 1:
        name1 = content[0]
        name2 = content[1]
    else:
        msg = '\n命令错误，例如：【/缘分 大熊 静香】'
        await catch_str9.finish(Message(f'{msg}'), at_sender=True)

    try:
        msg = await get_data9(name1, name2)
        await catch_str9.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str9.finish(Message(f'{msg}'), at_sender=True)


async def get_data9(name1, name2):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/yf.php?name1=' + name1 + '&name2=' + name2
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')


@catch_str10.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        msg = await get_data10(content)
        await catch_str10.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str10.finish(Message(f'{msg}'), at_sender=True)


async def get_data10(content):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/gujia.php?data=&qq=' + content
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')


@catch_str11.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        data_json = await get_data11(content)
        msg = json.dumps(data_json, indent=2, ensure_ascii=False)
        await catch_str11.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str11.finish(Message(f'{msg}'), at_sender=True)


async def get_data11(content):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/laji.php?msg=' + content
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                result = await response.read()
                ret = json.loads(result)
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret


@catch_str12.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        msg = await get_data12(content)
        await catch_str12.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str12.finish(Message(f'{msg}'), at_sender=True)


async def get_data12(content):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/wb_dx.php?msg=' + content
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')


@catch_str13.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        data_json = await get_tb_data(content)
        msg = json.dumps(data_json, indent=2, ensure_ascii=False)
        await catch_str13.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str13.finish(Message(f'{msg}'), at_sender=True)


@catch_str14.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        data_json = await get_bd_data(content)
        msg = json.dumps(data_json, indent=2, ensure_ascii=False)
        await catch_str14.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str14.finish(Message(f'{msg}'), at_sender=True)


async def get_tb_data(content):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/taobaoword.php?msg=' + content
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                result = await response.read()
                ret = json.loads(result)
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret


async def get_bd_data(content):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/wl/baiduword.php?msg=' + content
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                result = await response.read()
                ret = json.loads(result)
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret


@catch_str15.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    try:
        data_json = await get_data15(content)

        msg = data_json['msg']
        await catch_str15.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str15.finish(Message(f'{msg}'), at_sender=True)


async def get_data15(content):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/emoji_change.php?msg=' + content
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                result = await response.read()
                ret = json.loads(result)
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret


@catch_str16.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        msg = await get_data16(content)
        await catch_str16.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str16.finish(Message(f'{msg}'), at_sender=True)


@catch_str17.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        msg = await get_data16(content, 1)
        await catch_str17.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str17.finish(Message(f'{msg}'), at_sender=True)


async def get_data16(msg, type=None):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/url.php?data=&msg=' + msg + '&type='
        if type != None:
            API_URL += str(type)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')


@catch_str18.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        msg = await get_data18(content)
        await catch_str18.finish(Message(f'{msg}'), at_sender=True)
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await catch_str18.finish(Message(f'{msg}'), at_sender=True)


async def get_data18(content):
    try:
        API_URL = 'https://xiaobai.klizi.cn/API/other/pdzs.php?data=&msg=' + content
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL) as response:
                ret = await response.read()
    except Exception as e:
        nonebot.logger.info(e)
        return None
    
    return ret.decode('utf-8')

