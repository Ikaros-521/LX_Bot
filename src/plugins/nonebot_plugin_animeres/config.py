from typing import Optional
from pydantic import BaseModel
from nonebot import get_driver


class Config(BaseModel):
    # 设置代理端口
    cartoon_proxy: Optional[str] = None
    # 合并转发的形式发送消息
    cartoon_forward: bool = True
    # 每次发送的数量，用-1表示全部取出
    cartoon_length: int = 5
    # 发送的消息格式化
    cartoon_formant: str = "{title}\n{magnet}"


global_config = Config(**get_driver().config.dict())

