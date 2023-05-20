import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random, json

catch_str = on_command('生草')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event):
    try:
        data = await get_img_url()
        if data is not None:
            msg = MessageSegment.image(file="https://oss.grass.starxw.com/service/image?id=" + str(data))
    except Exception as e:
        nonebot.logger.info(e)
        msg = "\n请求失败，可能是网络问题或者是API寄了~"
    
    await catch_str.finish(Message(f'{msg}'), reply=True)


async def get_img_url():
    api_url = 'https://oss.grass.starxw.com/service/info?rand=' + str(random.randint(1, 10000))
    # header1 = {
    #     'content-type': 'text/plain; charset=utf-8',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
    # }

    # 捕获可能出现的异常
    try:
        # 创建一个异步的aiohttp.ClientSession对象，该对象可以管理HTTP连接和请求。使用async with语句可以确保在请求完成后正确关闭连接。
        async with aiohttp.ClientSession() as session:
            # 使用ClientSession对象的get方法发送HTTP GET请求。url参数指定请求的URL。使用async with语句可以确保请求完成后正确关闭响应对象。
            async with session.get(url=api_url) as response:
                # 从响应中读取原始字节数据，并使用await等待响应的完成。
                result = await response.read()
                # 将原始字节数据解析为Python数据类型。在这里，json.loads方法将JSON格式的数据转换为Python字典或列表。
                data_json = json.loads(result)
                # 使用Nonebot框架提供的logger日志记录器对象，打印JSON数据的信息。
                # nonebot.logger.info(data_json)

                # 返回id
                return data_json['id']
    # 如果try块中发生异常，则执行except块中的代码。这里的Exception是Python中所有异常的基类，它可以捕获任何异常。
    except Exception as e:
        # 打印异常信息
        nonebot.logger.info(e)
        # 返回空值，表示函数未能成功获取JSON数据
        return None
