from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.plugin import on_message
from .log import logger
from .config2 import config_contain
from .rule import rule_checker
from asyncio import sleep

import nonebot
from .config import Config
from .data_source import translate_msg, LANGUAGES
from .utils import EXCEPTIONS
from typing import Tuple, Any

from nonebot import on_regex
from nonebot.params import RegexGroup
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.exception import FinishedException

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

CONFIGS = config_contain.contains
DANGER = {"xml", "cardimage"}  # xml, cardimage 易风控
MAPPING = {
    "record": "语音",
    "video": "视频",
    "music": "音乐",
    "json": "分享",
    "forward": "合并",
}

listen = on_message(rule=rule_checker)


@listen.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = event.message
    user_info = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
    group_info = await bot.get_group_info(group_id=event.group_id)

    for cfg in CONFIGS:
        if not cfg.state:
            continue

        cfg.state = False
        for group in cfg.send_groups:
            if cfg.msg_type == "plain" or cfg.msg_type == "reply":

                _query = msg.extract_plain_text().strip()

                _query = _query.replace("\r\n", ".")

                _from, _to = "x", "中"

                _from_to = [_from, _to]
                
                if len(_query) > 2000:
                    continue
                try:
                    await bot.send_group_msg(group_id=event.group_id, message=await translate_msg(_from_to, _query))
                except FinishedException:
                    pass
                except Exception as e:
                    logger.info(e)
