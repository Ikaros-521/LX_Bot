# 安装相关依赖库（别告诉我你没装nb
# pip install aiohttp （发送HTTP请求用）
import json
import aiohttp
import random
import os, traceback
from pathlib import Path

import nonebot
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.exception import FinishedException

config_data = {
    "api_ip_port": "http://127.0.0.1:7861",
    "chat_type": "知识库",
    "knowledge_base_id": "",
    "history_enable": True,
    "history_max_len": 500
}

# 获取env配置
try:
    nonebot.logger.debug(nonebot.get_driver().config.langchain_chatglm_api_ip_port)
    nonebot.logger.debug(nonebot.get_driver().config.langchain_chatglm_chat_type)
    nonebot.logger.debug(nonebot.get_driver().config.langchain_chatglm_knowledge_base_id)
    nonebot.logger.debug(nonebot.get_driver().config.langchain_chatglm_history_enable)
    nonebot.logger.debug(nonebot.get_driver().config.langchain_chatglm_history_max_len)
    config_data["api_ip_port"] = nonebot.get_driver().config.langchain_chatglm_api_ip_port
    config_data["chat_type"] = nonebot.get_driver().config.langchain_chatglm_chat_type
    config_data["knowledge_base_id"] = nonebot.get_driver().config.langchain_chatglm_knowledge_base_id
    config_data["history_enable"] = nonebot.get_driver().config.langchain_chatglm_history_enable
    config_data["history_max_len"] = nonebot.get_driver().config.langchain_chatglm_history_max_len
except:
    nonebot.logger.warning("langchain_chatglm配置有误，请排查！")

# 调用别人的API时候，要求你传入一个参数这种。然后以回复的形式返回
cmd7 = on_command('glm')

class Langchain_ChatGLM:
    def __init__(self, data):
        self.api_ip_port = data["api_ip_port"]
        self.chat_type = data["chat_type"]
        self.knowledge_base_id = data["knowledge_base_id"]
        self.history_enable = data["history_enable"]
        self.history_max_len = data["history_max_len"]

        self.history = []

    async def get_list_knowledge_base(self):
        url = self.api_ip_port + "/local_doc_qa/list_knowledge_base"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()  # 检查响应的状态码
                    result = await response.text()
                    ret = json.loads(result)

                    nonebot.logger.debug(ret)
                    nonebot.logger.info(f"本地知识库列表：{ret['data']}")

                    return ret['data']
        except Exception as e:
            nonebot.logger.error(traceback.format_exc())
            return None

    async def get_resp(self, prompt):
        """请求对应接口，获取返回值

        Args:
            prompt (str): 你的提问

        Returns:
            str: 返回的文本回答
        """
        try:
            if self.chat_type == "模型":
                data_json = {
                    "question": prompt, 
                    "streaming": False,
                    "history": self.history
                }
                url = self.api_ip_port + "/chat"
            elif self.chat_type == "知识库":
                data_json = {
                    "knowledge_base_id": self.knowledge_base_id,
                    "question": prompt, 
                    "streaming": False,
                    "history": self.history
                }
                url = self.api_ip_port + "/local_doc_qa/local_doc_chat"
            elif self.chat_type == "必应":
                data_json = {
                    "question": prompt, 
                    "history": self.history
                }
                url = self.api_ip_port + "/local_doc_qa/bing_search_chat"
            else:
                data_json = {
                    "question": prompt, 
                    "streaming": False,
                    "history": self.history
                }
                url = self.api_ip_port + "/chat"

            async with aiohttp.ClientSession() as session:
                async with session.post(url=url, json=data_json) as response:
                    response.raise_for_status()  # 检查响应的状态码
                    result = await response.text()
                    ret = json.loads(result)

                    nonebot.logger.debug(ret)
                    if self.chat_type == "问答库" or self.chat_type == "必应":
                        nonebot.logger.info(f'源自：{ret["source_documents"]}')

                    resp_content = ret['response']

                    # 启用历史就给我记住！
                    if self.history_enable:
                        while True:
                            # 获取嵌套列表中所有字符串的字符数
                            total_chars = sum(len(string) for sublist in self.history for string in sublist)
                            # 如果大于限定最大历史数，就剔除第一个元素
                            if total_chars > self.history_max_len:
                                self.history.pop(0)
                            else:
                                self.history.append(ret['history'][-1])
                                break

                    return resp_content
        except Exception as e:
            nonebot.logger.error(traceback.format_exc())
            return None


langchain_chatglm = Langchain_ChatGLM(config_data)

@cmd7.handle()
async def _(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        # 发送get请求，调用API获取返回的文本赋值给msg，接口是统计字数的
        msg = await langchain_chatglm.get_resp(content)
        # 返回的data_json如果是None的话 就是请求中出问题了
        if None == msg:
            msg = "\n请求异常，可能是网络问题或者API挂了喵~（请检查后台日志排查）"
        # 设置 reply_message 参数为 True，表示回复原来的消息
        await cmd7.finish(Message(f'{msg}'), reply_message=True)
    # FinishedException，指示 NoneBot 结束当前 Handler 且后续 Handler 不再被运行。可用于结束用户会话。
    except FinishedException:
        pass
    except Exception as e:
        # 打印下异常报错
        nonebot.logger.info(e)
        msg = '\n请求失败喵（看看后台日志吧）'
        await cmd7.finish(Message(f'{msg}'), reply_message=True)


