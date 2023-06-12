from nonebot.adapters.onebot.v11 import Message
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg
import nonebot

import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

CLAUDE_API_KEY = "请在.env.xx中配置喵"
CLAUDE_PROXY = "请在.env.xx中配置喵"
CLAUDE_USER_ID = "请在.env.xx中配置喵"

# 获取env配置
try:
    nonebot.logger.debug(nonebot.get_driver().config.claude_api_key)
    CLAUDE_API_KEY = nonebot.get_driver().config.claude_api_key
except:
    CLAUDE_API_KEY = ""
    nonebot.logger.warning("claude_api_key没有配置，功能无法使用喵~。")

try:
    nonebot.logger.debug(nonebot.get_driver().config.claude_user_id)
    CLAUDE_USER_ID = nonebot.get_driver().config.claude_user_id
except:
    CLAUDE_USER_ID = ""
    nonebot.logger.warning("claude_user_id没有配置，功能无法使用喵~。")

try:
    nonebot.logger.debug(nonebot.get_driver().config.claude_proxy)
    CLAUDE_PROXY = nonebot.get_driver().config.claude_proxy
except:
    CLAUDE_PROXY = None
    nonebot.logger.warning("claude_proxy没有配置，直连访问喵~。")

client = WebClient(token=CLAUDE_API_KEY, proxy=CLAUDE_PROXY)

catch_str = on_command('claude', aliases={"cld"})

def send_message(channel, text):
    try:
        return client.chat_postMessage(channel=channel, text=text)
    except SlackApiError as e:
        # print(f"Error sending message: {e}")
        nonebot.logger.info(f"Error sending message: {e}")
        return None

def fetch_messages(channel, last_message_timestamp):
    response = client.conversations_history(channel=channel, oldest=last_message_timestamp)
    return [msg['text'] for msg in response['messages'] if msg['user'] == CLAUDE_USER_ID]

def get_new_messages(channel, last_message_timestamp):
    timeout = 60  # 超时时间设置为60秒
    start_time = time.time()

    while True:
        messages = fetch_messages(channel, last_message_timestamp)
        if messages and not messages[-1].endswith('Typing…_'):
            return messages[-1]
        if time.time() - start_time > timeout:
            return None
        
        time.sleep(5)

def find_direct_message_channel(user_id):
    try:
        response = client.conversations_open(users=user_id)
        return response['channel']['id']
    except SlackApiError as e:
        # print(f"Error opening DM channel: {e}")
        nonebot.logger.info(f"Error opening DM channel: {e}")
        return None


dm_channel_id = find_direct_message_channel(CLAUDE_USER_ID)
if not dm_channel_id:
    # print("Could not find DM channel with the bot.")
    nonebot.logger.error("Could not find DM channel with the bot.")
    exit

last_message_timestamp = None


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    response = send_message(dm_channel_id, content)
    if response:
        last_message_timestamp = response['ts']
    else:
        await catch_str.finish(Message('请求失败，请检查后台日志排查问题'), reply_message=True)

    new_message = get_new_messages(dm_channel_id, last_message_timestamp)
    if new_message == None:
        await catch_str.finish(Message('请求超时，无数据返回...'), reply_message=True)
    await catch_str.finish(Message(f'{new_message}'), reply_message=True)