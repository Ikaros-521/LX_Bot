from pydantic import BaseModel
from typing import Dict, List

class Config(BaseModel):
    # 需要监听的群号列表
    keyword_reply_target_groups: List[int] = []
    # 关键词回复配置 {关键词: 回复内容}
    keyword_reply_json: Dict[str, str] = {
        "你好": "你好啊！",
        "早安": "早安！今天也要元气满满哦！",
        "晚安": "晚安！做个好梦~"
    } 