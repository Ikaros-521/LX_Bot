import re
from enum import Enum
from typing import Optional, Literal, List

from pydantic import BaseModel, Extra, validator

from nonebot.log import logger

from .exceptions import (
    BaseBingChatException,
    BingChatResponseException,
    BingChatAccountReachLimitException,
    BingChatConversationReachLimitException,
)


class filterMode(str, Enum):
    whitelist = 'whitelist'
    blacklist = 'blacklist'


class Config(BaseModel):
    superusers: List[int] = []
    command_start: List[str] = ['']

    bingchat_conversation_style: Literal['creative', 'balanced', 'precise'] = 'balanced'

    bingchat_command_chat: List[str] = ['chat']
    bingchat_command_new_chat: List[str] = ['chat-new', '刷新对话']
    bingchat_command_history_chat: List[str] = ['chat-history']
    bingchat_to_me: bool = False

    bingchat_auto_refresh_conversation: bool = False

    bingchat_limit_rate: Optional[int] = None  # 未实现
    bingchat_limit_count: Optional[int] = None  # 未实现

    bingchat_group_filter_mode: filterMode = filterMode.blacklist
    bingchat_group_filter_blacklist: List[int] = []
    bingchat_group_filter_whitelist: List[int] = []

    @validator('bingchat_command_chat', pre=True)
    def bingchat_command_chat_validator(cls, v):
        if not v:
            raise ValueError('bingchat_command_chat不能为空')
        return list(v)

    @validator('bingchat_command_new_chat', pre=True)
    def bingchat_command_new_chat_validator(cls, v):
        if not v:
            raise ValueError('bingchat_command_new_chat不能为空')
        return list(v)

    @validator('bingchat_command_history_chat', pre=True)
    def bingchat_command_history_chat_validator(cls, v):
        if not v:
            raise ValueError('bingchat_command_history_chat不能为空')
        return list(v)


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
        from .utils import removeQuoteStr

        try:
            return removeQuoteStr(self.raw["item"]["messages"][1]["text"])
        except (IndexError, KeyError) as exc:
            logger.error(self.raw)
            raise BingChatResponseException('<无效的响应值, 请管理员查看控制台>') from exc


class Conversation(BaseModel):
    ask: str
    reply: BingChatResponse
