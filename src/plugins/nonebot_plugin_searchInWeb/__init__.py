import nonebot
# from io import BytesIO
from nonebot import on_keyword, on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.params import CommandArg
# from nonebot_plugin_imageutils import Text2Image
from nonebot_plugin_htmlrender import (
    # text_to_pic,
    md_to_pic,
    # template_to_pic,
    get_new_page,
)


from nonebot.plugin import PluginMetadata


help_text = f"""
插件功能：
/bd 这是百度
/百度 搜索内容
/bing 这是必应
/必应 搜索内容

""".strip()

__plugin_meta__ = PluginMetadata(
    name = '搜索引擎截图',
    description = '适用于nonebot2 v11的搜索引擎截图',
    usage = help_text
)


# 所有的命令都在这哦，要改命令触发关键词的请自便
catch_str = on_command("百度", aliases={"bd"})
catch_str2 = on_command('必应', aliases={"bing"})


# 
@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    try:
        async with get_new_page(viewport={"width": 800, "height": 200}) as page:
            await page.goto(
                "https://www.baidu.com/s?wd=" + content,
                timeout=2 * 60 * 1000,
                wait_until="networkidle",
            )
            pic = await page.screenshot(full_page=True, path="./data/baidu.png")

        await catch_str.finish(MessageSegment.image(pic))
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n打开页面失败喵（看看后台日志吧）'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)


# 
@catch_str2.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    try:
        async with get_new_page(viewport={"width": 800, "height": 200}) as page:
            await page.goto(
                "https://cn.bing.com/search?FORM=BESBTB&q=" + content,
                timeout=2 * 60 * 1000,
                wait_until="networkidle",
            )
            pic = await page.screenshot(full_page=True, path="./data/bing.png")

        await catch_str2.finish(MessageSegment.image(pic))
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(e)
        msg = '\n查打开页面失败喵（看看后台日志吧）'
        await catch_str2.finish(Message(f'{msg}'), at_sender=True)
