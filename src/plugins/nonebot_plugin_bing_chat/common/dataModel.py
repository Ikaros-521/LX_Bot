import re
from enum import Enum
from typing import Optional

from EdgeGPT import Chatbot
from pydantic import BaseModel, Extra, validator

from nonebot.log import logger

from typing import List, Optional, Union

from .exceptions import (
    BaseBingChatException,
    BingChatResponseException,
    BingChatAccountReachLimitException,
    BingChatConversationReachLimitException,
)


class filterMode(str, Enum):
    whitelist = 'whitelist'
    blacklist = 'blacklist'


class Config(BaseModel, extra=Extra.ignore):
    superusers: List[int] = []
    command_start: Union[str, List[str]] = []

    bingchat_command_chat: Union[str, List[str]] = ['chat']
    bingchat_command_new_chat: Union[str, List[str]] = ['chat-new', '刷新对话']
    bingchat_command_history_chat: Union[str, List[str]] = ['chat-history']

    bingchat_auto_refresh_conversation: bool = False

    bingchat_command_limit_rate: Optional[int] = None # 未实现
    bingchat_command_limit_count: Optional[int] = None # 未实现

    bingchat_group_filter_mode: str = 'blacklist'
    bingchat_group_filter_blacklist: List[int] = []
    bingchat_group_filter_whitelist: List[int] = []

    @validator('bingchat_command_chat')
    def bingchat_command_chat_validator(cls, v):
        return list(v)

    @validator('bingchat_command_new_chat')
    def bingchat_command_new_chat_validator(cls, v):
        return list(v)


class BingChatResponse(BaseModel):
    raw: dict

    @validator('raw')
    def rawValidator(cls, v):
        if v['item']['result']['value'] == 'Success':
            numUserMessagesInConversation = v['item']['throttling']['numUserMessagesInConversation']
            maxNumUserMessagesInConversation = v['item']['throttling']['maxNumUserMessagesInConversation']
            if numUserMessagesInConversation > maxNumUserMessagesInConversation:
                raise BingChatConversationReachLimitException(
                    f'<达到对话上限>\n'
                    f'最大对话次数：{maxNumUserMessagesInConversation}\n'
                    f'你的话次数：{numUserMessagesInConversation}'
                )
            return v
        elif v['item']['result']['value'] == 'Throttled':
            logger.error('<Bing账号到达今日请求上限>')
            raise BingChatAccountReachLimitException('<Bing账号到达今日请求上限>')

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
