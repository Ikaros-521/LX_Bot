# 安装相关依赖库（别告诉我你没装nb
# pip install aiohttp （发送HTTP请求用）
import json
import aiohttp
import random
import os
from pathlib import Path

import nonebot
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.params import CommandArg


# 获取当前命令型消息的元组形式命令名，简单说就是 触发的命令（不含命令前缀）
cmd1 = on_command('本地图片', aliases={"本地图片别名"})
# 那么下面这行就是 触发命令为 狗狗图 或者 狗狗图别名 。 其中 aliases是命令的别名，都可以触发。
cmd2 = on_command('狗狗图', aliases={"狗狗图别名"})
cmd3 = on_command('本地图片含传参')

# 读取本地文件中的内容返回
cmd4 = on_command('本地文件')

# 固定命令触发，直接返回固定文本
cmd5 = on_command('固定文本')
# 固定命令 追加一个传参 触发，直接返回对应的固定文本
cmd6 = on_command('固定文本含传参')


@cmd1.handle()
async def _(bot: Bot, event: MessageEvent):
    # 文件路径 绝对或相对路径，多余的注释了，下面只是演示
    # 可以是相对路径 ./ 当前路径（运行nb run的路径 即 bot项目根路径），当前路径下的data/template文件夹下的1.png
    file_path = "./data/template/1.png"
    # 可以是绝对路径（自行替换哈 Linux）
    file_path = "/root/LX_Bot/data/template/1.png"
    # 可以是绝对路径（自行替换哈 windows）, 我这边是项目内的data/template文件夹下的1.png
    file_path = "E:\\GitHub_pro\\LX_Bot\\data\\template\\1.png"

    try:
        # 使用数据项file_path中的文件路径创建一个Path对象
        path = Path(file_path)
        # 使用MessageSegment.image方法创建一个消息段，该消息段包含了文件路径对应的图像文件，并将其赋值给变量msg。
        # 在这个过程中，代码通过file参数将文件路径传递给image方法，以指定要发送的图像文件
        # file支持很多类型 Union[str, bytes, BytesIO, Path]，可以看看源码
        msg = MessageSegment.image(file=path)
    except Exception as e:
        # 如果循环没有被中断，即所有的数据项都被遍历完，就执行这个语句块
        # msg 为 字符串信息
        msg = '\n发送失败喵，请检查后台日志排查问题~'
    # 返回msg信息 结束，并且@触发命令的人（at_sender=True），不需要@可以改为False或者删掉
    await cmd1.finish(Message(msg), at_sender=True)


# 使用 cmd2 响应器的 handle 装饰器装饰了一个函数_， _函数会被自动转换为 Dependent 对象，并被添加到 cmd2 的事件处理流程中
# 简单点 保持一直就行
@cmd2.handle()
# 获取当前事件的 Bot 对象。 其实这里没用到
# 获取当前事件 MessageEvent。 可以判断消息来源等
# 获取命令型消息命令后跟随的参数 CommandArg。 获取传入的参数，解析处理
async def _(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    # 调用了msg对象的extract_plain_text方法，该方法用于从消息对象中提取纯文本内容。它会自动去除消息中的所有格式和特殊字符，只返回包含文本的部分。
    # 接着，strip方法被用于去除返回的字符串的首尾空格
    content = msg.extract_plain_text().strip()
    # 打印日志 传参内容content，可以看看
    nonebot.logger.info(content)
    # 等待请求函数返回我们需要的结果，赋值给data_json
    data_json = await get_api_return_img_json2()
    if None == data_json:
        # 调用了NoneBot框架中的finish方法，该方法用于结束一个会话，并发送一个消息作为会话的最终结果
        # 我们发送一个字符串 结束
        await cmd2.finish("请求失败，这里写相关的错误的提示内容，告诉用户失败了")
    # 获取data_json的message键对应的值，这个例子里是个url（带\\）,所以加上了replace将\\给替换成空
    url = data_json["message"].replace('\\', '')
    # 调用了NoneBot框架中的finish方法，该方法用于结束一个会话，并发送一个消息作为会话的最终结果
    # finish里面调用了MessageSegment对象的image方法，该方法用于构造一个图片消息段。file参数指定了图片文件的URL，该图片将被发送给机器人用户。
    # await关键字用于等待消息的发送操作完成，以避免异步消息发送的竞争条件
    await cmd2.finish(MessageSegment.image(file=url))


@cmd3.handle()
async def _(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    # 打印日志 传参内容content，可以看看
    nonebot.logger.info(content)
    # 构建了json存储 传参关键词 和 返回的内容
    data_json = [
        {
            "keyword": "图片1",
            # 可以是相对路径 ./ 当前路径（运行nb run的路径 即 bot项目根路径），当前路径下的data/template文件夹下的1.png
            "msg": "./data/template/1.png"
        },
        {
            "keyword": "图片2",
            # 可以是绝对路径（自行替换哈 windows）, 我这边是项目内的data/template文件夹下的1.png
            "msg": "E:\\GitHub_pro\\LX_Bot\\data\\template\\1.png"
        },
        {
            "keyword": "图片3",
            # 可以是绝对路径（自行替换哈 Linux）
            "msg": "/root/LX_Bot/data/template/1.png"
        }
    ]
    # 循环遍历data_json数据源中的所有数据项
    for item in data_json:
        # 查找与用户输入的传参关键词content 匹配的数据项 item["keyword"]
        if content == item["keyword"]:
            # 将对应的msg值赋值给path_str
            path_str = item["msg"]
            # 使用数据项path_str中的文件路径创建一个Path对象
            path = Path(path_str)
            # 使用MessageSegment.image方法创建一个消息段，该消息段包含了文件路径对应的图像文件，并将其赋值给变量msg。
            # 在这个过程中，代码通过file参数将文件路径传递给image方法，以指定要发送的图像文件
            # file支持很多类型 Union[str, bytes, BytesIO, Path]，可以看看源码
            msg = MessageSegment.image(file=path)
            # 退出循环
            break
    else:
        # 如果循环没有被中断，即所有的数据项都被遍历完，就执行这个语句块
        # msg 为 字符串信息
        msg = '\n果咩，没有此关键词的索引，请联系bot管理员添加~'
    # 返回msg信息 结束，并且@触发命令的人（at_sender=True），不需要@可以改为False或者删掉
    await cmd3.finish(Message(msg), at_sender=True)


@cmd4.handle()
async def _(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    # 打印日志 传参内容content，可以看看
    nonebot.logger.info(content)
    # 构建了json存储 传参关键词 和 本地文件路径
    data_json = [
        {
            "keyword": "文件1",
            # 可以是相对路径 ./ 当前路径（运行nb run的路径 即 bot项目根路径），当前路径下的data文件夹下的1.png
            "msg": "./data/template/1.txt"
        },
        {
            "keyword": "文件2",
            # 可以是绝对路径（自行替换哈 windows）, 我这边是项目内的data文件夹下的1.png
            "msg": "E:\\GitHub_pro\\LX_Bot\\data\\template\\1.txt"
        },
        {
            "keyword": "文件3",
            # 可以是绝对路径（自行替换哈 Linux）
            "msg": "/root/LX_Bot/data/template/1.txt"
        }
    ]
    # 循环遍历data_json数据源中的所有数据项
    for item in data_json:
        # 查找与用户输入的传参关键词content 匹配的数据项 item["keyword"]
        if content == item["keyword"]:
            # 将对应的msg值赋值给path_str
            path_str = item["msg"]
            # 检查指定的文件path_str是否存在
            if os.path.exists(path_str):
                # 异常捕获 方便定位问题并让bot有所反馈
                try:
                    # 以只读模式打开文件，以UTF-8编码方式读取文件内容。如果文件不存在或无法打开，则会引发异常。
                    with open(path_str, 'r', encoding='utf-8') as f:
                        # 如果文件成功打开，则使用read()方法读取文件内容，并将其存储在变量msg中。
                        msg = f.read()
                        # 关闭文件句柄
                        f.close()
                except Exception as e:
                    # 如果发生异常，则将异常信息记录到后台日志中，并将msg变量设置为一个错误消息，提示用户文件读取失败。
                    nonebot.logger.info(e)
                    msg = '\n读取本地文件数据失败，请检查后台日志定位问题~'
            else:
                # 文件不存在，给出错误提示
                msg = '\n文件不存在，请检查文件路径~'
            # 退出循环
            break
    else:
        # 如果循环没有被中断，即所有的数据项都被遍历完，就执行这个语句块
        # msg 为 字符串信息
        msg = '\n果咩，没有此关键词的索引，请联系bot管理员添加~'
    # 返回msg信息 结束，并且@触发命令的人（at_sender=True），不需要@可以改为False或者删掉
    await cmd3.finish(Message(msg), at_sender=True)


@cmd5.handle()
async def _(bot: Bot, event: MessageEvent):
    # 文本赋值给msg
    msg = "这是一个固定的句子，自行编辑即可。"
    # 返回msg信息 结束，并且@触发命令的人（at_sender=True），不需要@可以改为False或者删掉
    await cmd5.finish(Message(msg), at_sender=True)


@cmd6.handle()
async def _(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()
    # 打印日志 传参内容content，可以看看
    nonebot.logger.info(content)
    # 构建了json存储 传参关键词 和 返回的内容
    data_json = [
        {
            "keyword": "关键词1",
            # msg是返回的文本
            "msg": "这是一个普通的句子，123abc@#$"
        },
        {
            "keyword": "关键词2",
            "msg": "链接：www.baidu.com"
        },
        {
            "keyword": "关键词3",
            # 下面这个插件项目 功能是根据传参的文本，拼接发病语录，然后返回
            "msg": "随机发病语录：https://github.com/Ikaros-521/nonebot_plugin_random_stereotypes"
        }
    ]
    # 循环遍历data_json数据源中的所有数据项
    for item in data_json:
        # 查找与用户输入的传参关键词content 匹配的数据项 item["keyword"]
        if content == item["keyword"]:
            # 将对应的msg值赋值给msg
            msg = item["msg"]
            # 退出循环
            break
    else:
        # 如果循环没有被中断，即所有的数据项都被遍历完，就执行这个语句块
        # msg 为 字符串信息
        msg = '\n果咩，没有此关键词的索引，请联系bot管理员添加~'
    # 返回msg信息 结束，并且@触发命令的人（at_sender=True），不需要@可以改为False或者删掉
    await cmd6.finish(Message(msg), at_sender=True)



# 异步 get请求API，API返回一个JSON格式的数据转换为Python字典返回
async def get_api_return_img_json2():
    # API的地址，get传参也直接拼接上
    api_url = 'https://dog.ceo/api/breeds/image/random?' + str(random.random())
    
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
                nonebot.logger.info(data_json)
                # 返回Python数据类型的JSON数据
                return data_json
    # 如果try块中发生异常，则执行except块中的代码。这里的Exception是Python中所有异常的基类，它可以捕获任何异常。
    except Exception as e:
        # 打印异常信息
        nonebot.logger.info(e)
        # 返回空值，表示函数未能成功获取JSON数据
        return None
