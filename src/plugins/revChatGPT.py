from nonebot import on_command
import nonebot
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.typing import T_State
# from nonebot.params import CommandArg
from revChatGPT.revChatGPT import Chatbot
import time

# chatGPT = on_command("", priority=7, block=True)
chatGPT = on_command("gpt")
user_chatbot = dict()


# Get your config in JSON
config = {
        "Authorization": "<Your Bearer Token Here>", # This is optional
        "session_token": ""
}

def ask(user, msg):
    chatbot = None
    if user in user_chatbot:

        bot_time = user_chatbot[user][1]
        if time.time() < bot_time + 60 * 2:
            chatbot = user_chatbot[user][0]
        else:
            # 如果上一次会话超过三分钟则开启新的会话
            chatbot = user_chatbot[user][0]
            chatbot.reset_chat()
    else:
        chatbot = Chatbot(config, conversation_id=None)

    chatbot.refresh_session()
    resp = chatbot.get_chat_response(msg)
    user_chatbot[user] = [chatbot, time.time()]
    return resp['message']

@chatGPT.handle()
async def _(bot: Bot, event: Event, state: T_State):
    user = event.get_user_id()
    msg = event.get_plaintext().strip()[4:]
    # nonebot.logger.info("msg:" + msg)
    # msg = arg.extract_plain_text().strip()
    r = ask(user, msg)
    res = MessageSegment.at(user) + '\n' + r
    await chatGPT.send(res)