import re
from enum import Enum
from typing import Optional, Literal, List, Set
from pathlib import Path

from pydantic import BaseModel, Extra, validator

from nonebot.log import logger

from .exceptions import (
    BaseBingChatException,
    BingChatResponseException,
    BingChatAccountReachLimitException,
    BingChatConversationReachLimitException,
)


def removeQuoteStr(string: str) -> str:
    return re.sub(r'\[\^\d+?\^\]', '', string)


class filterMode(str, Enum):
    whitelist = 'whitelist'
    blacklist = 'blacklist'


class Config(BaseModel):
    superusers: Set[int] = set()

    bingchat_block: bool = False
    bingchat_to_me: bool = False
    bingchat_priority: int = 1
    bingchat_share_chat: bool = False
    bingchat_command_start: Set[str] = {'/'}

    bingchat_command_chat: Set[str] = {'chat'}
    bingchat_command_new_chat: Set[str] = {'chat-new', '刷新对话'}
    bingchat_command_history_chat: Set[str] = {'chat-history'}

    bingchat_log: bool = False
    bingchat_show_detail: bool = False
    bingchat_show_is_waiting: bool = True
    bingchat_plugin_directory: Path = Path('./data/BingChat')
    bingchat_conversation_style: str = 'balanced'
    bingchat_auto_refresh_conversation: bool = True

    bingchat_group_filter_mode: filterMode = filterMode.blacklist
    bingchat_group_filter_blacklist: Set[int] = set()
    bingchat_group_filter_whitelist: Set[int] = set()

    def __init__(self, **data) -> None:
        bingchat_command_start = data.pop('bingchat_command_start', {'/'})
        super().__init__(**data)
        self.bingchat_command_start = bingchat_command_start

    @validator('bingchat_command_chat', pre=True)
    def bingchat_command_chat_validator(cls, v: set) -> set:
        if not v:
            raise ValueError('bingchat_command_chat不能为空')
        return set(v)

    @validator('bingchat_command_new_chat', pre=True)
    def bingchat_command_new_chat_validator(cls, v: set) -> set:
        if not v:
            raise ValueError('bingchat_command_new_chat不能为空')
        return set(v)

    @validator('bingchat_command_history_chat', pre=True)
    def bingchat_command_history_chat_validator(cls, v: set) -> set:
        if not v:
            raise ValueError('bingchat_command_history_chat不能为空')
        return set(v)

    @validator('bingchat_plugin_directory', pre=True)
    def bingchat_plugin_directory_validator(cls, v: str) -> Path:
        return Path(v)

class BingChatResponse(BaseModel):
    raw: dict

    @validator('raw')
    def rawValidator(cls, v):
        if v['item']['result']['value'] == 'Success':
            num_conver = v['item']['throttling']['numUserMessagesInConversation']
            max_conver = v['item']['throttling']['maxNumUserMessagesInConversation']
            if num_conver > max_conver:
                raise BingChatConversationReachLimitException(
                    f'<达到对话上限>\n最大对话次数：{max_conver}\n你的话次数：{num_conver}'
                )
            if 'hiddenText' in v['item']['messages'][1]:
                raise BingChatResponseException(
                    f'<Bing检测到敏感问题，无法回答>\n'
                    f'{v["item"]["messages"][1]["hiddenText"]}'
                )
            return v
        elif v['item']['result']['value'] == 'Throttled':
            logger.error('<Bing账号到达今日请求上限>')
            raise BingChatAccountReachLimitException('<Bing账号到达今日请求上限>')
        else:
            logger.error('<未知的错误>')
            raise BingChatResponseException('<未知的错误, 请管理员查看控制台>')

    @property
    def content_simple(self) -> str:
        try:
            return removeQuoteStr(
                self.raw["item"]["messages"][1]["adaptiveCards"][0]['body'][0]['text']
            )
        except (IndexError, KeyError) as exc:
            logger.error(self.raw)
            raise BingChatResponseException('<无效的响应值, 请管理员查看控制台>') from exc
    @property
    def content_with_reference(self) -> str:
        try:
            return removeQuoteStr(
                self.raw["item"]["messages"][1]["adaptiveCards"][0]['body'][0]['text']
            )
        except (IndexError, KeyError) as exc:
            logger.error(self.raw)
            raise BingChatResponseException('<无效的响应值, 请管理员查看控制台>') from exc
    @property
    def content_detail(self) -> str:
        ...
    @property
    def adaptive_cards(self) -> list:
        try:
            return self.raw["item"]["messages"][1]["adaptiveCards"][0]['body']
        except (IndexError, KeyError) as exc:
            logger.error(self.raw)
            raise BingChatResponseException('<无效的响应值, 请管理员查看控制台>') from exc

class Conversation(BaseModel):
    ask: str
    reply: BingChatResponse
