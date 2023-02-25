from nonebot.adapters.onebot.v11 import GroupMessageEvent
from .config2 import Config2, config_contain
import re

configs = config_contain.contains


async def rule_checker(event: GroupMessageEvent) -> bool:
    """规则检查"""
    flag = False
    for cfg in configs:
        if all((
                group_checker(event, cfg),
                type_checker(event, cfg),
                user_checker(event, cfg),
                content_checker(event, cfg)
        )):
            cfg.state = True
            flag = True
    return flag


def type_checker(event: GroupMessageEvent, cfg: Config2) -> bool:
    """检查消息类型"""
    msg = event.raw_message
    contain_cq = re.findall(r"CQ:(.*?),", msg)
    if not contain_cq:  # 纯文本不含cq码
        cfg.msg_type = "plain"
        return "plain" in cfg.listen_type if cfg.listen_type else True

    cfg.msg_type = contain_cq[0]
    return contain_cq[0] in cfg.listen_type if cfg.listen_type else True


def group_checker(event: GroupMessageEvent, cfg: Config2) -> bool:
    """检查群"""
    return (
        event.group_id in cfg.listen_groups
        if cfg.listen_groups
        else True
    )


def user_checker(event: GroupMessageEvent, cfg: Config2) -> bool:
    """检查用户"""
    return (
        event.user_id in cfg.listen_users
        if cfg.listen_users
        else True
    )


def content_checker(event: GroupMessageEvent, cfg: Config2) -> bool:
    """检查消息内容"""
    return any(
        content in event.message
        for content in cfg.listen_content
    ) if cfg.listen_content else True


__all__ = [
    "rule_checker"
]