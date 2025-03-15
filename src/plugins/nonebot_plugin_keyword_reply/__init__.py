from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule
import nonebot

from .config import Config

# 插件元数据
__plugin_meta__ = PluginMetadata(
    name="关键词回复",
    description="监听指定群聊消息并进行关键词回复",
    usage="无需额外命令，自动监听并回复",
    type="application",
    homepage="https://github.com/your-username/nonebot_plugin_keyword_reply",
    supported_adapters={"~onebot.v11"},
)

# 获取配置
global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

def check_group(event: GroupMessageEvent) -> bool:
    """检查是否是目标群"""
    return event.group_id in plugin_config.keyword_reply_target_groups

# 创建消息匹配规则
def keyword_rule() -> Rule:
    async def _keyword_rule(event: GroupMessageEvent) -> bool:
        if not check_group(event):
            return False
        
        msg = event.get_plaintext()
        for keyword in plugin_config.keyword_reply_json.keys():
            if keyword in msg:
                return True
        return False
    
    return Rule(_keyword_rule)

# 注册消息响应器
keyword_matcher = on_message(rule=keyword_rule(), priority=10)

@keyword_matcher.handle()
async def handle_keyword(bot: Bot, event: GroupMessageEvent):
    msg = event.get_plaintext()
    
    # 遍历关键词字典，找到匹配的关键词并回复
    for keyword, reply in plugin_config.keyword_reply_json.items():
        if keyword in msg:
            await keyword_matcher.finish(reply) 