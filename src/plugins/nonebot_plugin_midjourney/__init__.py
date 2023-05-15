from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg
import nonebot
from nonebot.exception import FinishedException

import json
import re
import aiohttp
import asyncio
import pandas as pd
import os

catch_str = on_command('midj', aliases={"mj"})

default_json = {
    "channelid": "",
    "authorization": "",
    "application_id": "",
    "guild_id": "",
    "session_id": "",
    "version": "",
    "id": "",
    "flags": "--v 5",
    # "http://127.0.0.1:10809"
    "proxy": "",
    "timeout": 120
}

filename = 'config.json'
file_path = './data/nonebot_plugin_midjourney/'

if not os.path.exists(file_path):
    os.makedirs(file_path)

if not os.path.exists(os.path.join(file_path, filename)):
    with open(os.path.join(file_path, filename), 'w') as f:
        json.dump(default_json, f)
        nonebot.logger.info("nonebot_plugin_midjourney 配置文件初始化")


class Sender:

    def __init__(self, 
                 params):
        
        self.params = params
        self.sender_initializer()

    def sender_initializer(self):

        with open(self.params, "r") as json_file:
            params = json.load(json_file)

        self.channelid=params['channelid']
        self.authorization=params['authorization']
        self.application_id = params['application_id']
        self.guild_id = params['guild_id']
        self.session_id = params['session_id']
        self.version = params['version']
        self.id = params['id']
        self.flags = params['flags']
        if params['proxy'] != "":
            # 代理服务器的IP地址和端口号
            self.proxy = params['proxy']
        else:
            self.proxy = None
        
    async def send(self, prompt):
        header = {
            'authorization': self.authorization
        }
        
        prompt = prompt.replace('_', ' ')
        prompt = " ".join(prompt.split())
        prompt = re.sub(r'[^a-zA-Z0-9\s]+', '', prompt)
        prompt = prompt.lower()

        payload = {'type': 2, 
        'application_id': self.application_id,
        'guild_id': self.guild_id,
        'channel_id': self.channelid,
        'session_id': self.session_id,
        'data': {
            'version': self.version,
            'id': self.id,
            'name': 'imagine',
            'type': 1,
            'options': [{'type': 3, 'name': 'prompt', 'value': str(prompt) + ' ' + self.flags}],
            'attachments': []}
            }
        
        async with aiohttp.ClientSession() as session:
            retry = 3
            while retry >= 0:
                async with session.post('https://discord.com/api/v9/interactions', json=payload, headers=header, proxy=self.proxy) as resp:
                    if resp.status == 204:
                        break
                    
                    print(".", end="")
                retry -= 1

                if retry < 0:
                    return None

        # print(r.headers)
        # print(r.text)

        # print('prompt [{}] successfully sent!'.format(prompt))
        # prompt = prompt.replace(" ", "_")

        # 多个空格变一个空格
        prompt = re.sub(r'\s+', ' ', prompt)
        return prompt


class Receiver:

    def __init__(self, 
                 params,
                 prompt
                ):
        
        self.params = params
        self.prompt = prompt

        self.sender_initializer()

        self.df = pd.DataFrame(columns = ['prompt', 'url', 'filename', 'is_downloaded'])

    
    def sender_initializer(self):

        with open(self.params, "r") as json_file:
            params = json.load(json_file)

        self.channelid=params['channelid']
        self.authorization=params['authorization']
        self.headers = {'authorization' : self.authorization}
        if params['proxy'] != "":
            # 代理服务器的IP地址和端口号
            self.proxy = params['proxy']
        else:
            self.proxy = None
        self.timeout=params['timeout']

    async def retrieve_messages(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://discord.com/api/v10/channels/{self.channelid}/messages?limit={10}', headers=self.headers, proxy=self.proxy) as response:
                jsonn = await response.json()
        return jsonn

    async def collecting_results(self):
        # tmp_json = {
        #     "code": 0,
        #     "url": ""
        # }

        message_list  = await self.retrieve_messages()
        self.awaiting_list = pd.DataFrame(columns = ['prompt', 'status'])
        for message in message_list:
            try:
                # 如果这条消息是由"Midjourney Bot"发送的，并且包含双星号（**），则它是一个需要处理的请求
                if (message['author']['username'] == 'Midjourney Bot') and ('**' in message['content']):
                    # print(message)
                    if len(message['attachments']) > 0:
                        # 如果该消息包含图像附件，则获取该附件的URL和文件名，并将其添加到df DataFrame中
                        if (message['attachments'][0]['filename'][-4:] == '.png') or ('(Open on website for full quality)' in message['content']):
                            id = message['id']
                            prompt = message['content'].split('**')[1].split(' --')[0]
                            url = message['attachments'][0]['url']
                            filename = message['attachments'][0]['filename']

                            # print(f"prompt2=[{prompt}]")

                            # 判断prompt是否匹配
                            if self.prompt == prompt:
                                # DataFrame的索引是消息ID，因此我们可以根据消息ID来确定哪个请求与哪个消息相对应
                                if id not in self.df.index:
                                    self.df.loc[id] = [prompt, url, filename, 0]
                                    # print("filename=" + filename)
                                    # print("url=" + url)
                                    # tmp_json["url"] = url
                                    return url
                        # 如果消息中没有图像附件，则将该请求添加到awaiting_list DataFrame中，等待下一次检索。
                        else:
                            id = message['id']
                            prompt = message['content'].split('**')[1].split(' --')[0]
                            if ('(fast)' in message['content']) or ('(relaxed)' in message['content']):
                                try:
                                    status = re.findall("(\w*%)", message['content'])[0]
                                except:
                                    status = 'unknown status'
                            self.awaiting_list.loc[id] = [prompt, status]

                    else:
                        id = message['id']
                        prompt = message['content'].split('**')[1].split(' --')[0]
                        if '(Waiting to start)' in message['content']:
                            status = 'Waiting to start'
                        self.awaiting_list.loc[id] = [prompt, status]
            except Exception as e:
                print(e)

        return None


    async def check_result(self):
        for i in range(int(self.timeout / 3)):
            ret = await self.collecting_results()
            if ret != None:
                return ret
            # for i in self.df.index:
            #         return self.df.loc[i].url
            # 睡眠3s
            await asyncio.sleep(3)
        return None


    async def download_img(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, proxy=self.proxy) as response:
                return await response.read()


@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    config_path = file_path + filename

    sender = Sender(config_path)
    prompt = await sender.send(content)

    if prompt is not None:
        await catch_str.send(Message('请求已发送，请耐心等待...'), reply_message=True)
    else:
        await catch_str.finish(Message('请求失败'), reply_message=True)

    # print(f"prompt=[{prompt}]")

    receiver = Receiver(config_path, prompt)
    result = await receiver.check_result()

    try:
        if result is not None:
            # print(f"result=[{result}]")
            result = await receiver.download_img(result)
            await catch_str.finish(Message(MessageSegment.image(result)), reply_message=True)

        await catch_str.finish(Message('请求超时，无数据返回...'), reply_message=True)
    except FinishedException:
        pass
    except Exception as e:
        print(e)
        await catch_str.finish(Message('请求失败，请检查后台日志'), reply_message=True)
