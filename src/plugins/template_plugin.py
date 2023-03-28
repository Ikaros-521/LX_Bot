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
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.exception import FinishedException


# 获取当前命令型消息的元组形式命令名，简单说就是 触发的命令（不含命令前缀）
# 你测试的时候，可以看下你 env的配置中的命令起始字符 COMMAND_START，根据你的命令前缀加上cmd的命令词即可。
# 例如 COMMAND_START=["/"]  cmd1的触发命令（【】内的是命令啊，别把【】也打进去了）就是 【/本地图片】 或者 【/本地图片别名】
# 需要传参数的命令，例如cmd3的触发命令就是 【/本地图片含传参 图片1】
cmd1 = on_command('本地图片', aliases={"本地图片别名"})
# 那么下面这行就是 触发命令为 狗狗图 或者 狗狗图别名 。 其中 aliases是命令的别名，都可以触发。
cmd2 = on_command('狗狗图', aliases={"狗狗图别名"})
cmd3 = on_command('本地图片含传参')

# 读取本地文件中的内容返回 
cmd4 = on_command('本地文件含传参')

# 固定命令触发，直接返回固定文本
cmd5 = on_command('固定文本')
# 固定命令 追加一个传参 触发，直接返回对应的固定文本
cmd6 = on_command('固定文本含传参')

# 调用别人的API时候，要求你传入一个参数这种。然后以回复的形式返回
# 例子：传入 年-月-日 计算生肖
cmd7 = on_command('生肖计算')

# 图片+文字 合并转发
cmd8 = on_command('合并转发')


@cmd1.handle()
# 获取当前事件的 Bot 对象。 其实这里没用到
# 获取当前事件 MessageEvent。 可以判断消息来源等 这里也没用到。可以自行删除
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
    # 返回的data_json如果是None的话 就是请求中出问题了
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


@cmd7.handle()
async def _(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    try:
        # 发送get请求，调用API获取返回的文本赋值给msg
        msg = await get_api_return_txt(content)
        # 我们把提示语追加到返回的字符串句前，方便用户理解
        msg = "返回结果：" + msg
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


@cmd8.handle()
async def _(bot: Bot, event: MessageEvent):
    # 判断信息源自 群聊或私聊
    msg_from = "group"
    # 使用 isinstance() 函数来判断收到的事件类型是不是 GroupMessageEvent 类型
    if isinstance(event, GroupMessageEvent):
        # nonebot.logger.info("群聊")
        # 获取群聊的 group_id
        group = str(event.group_id)
    else:
        # nonebot.logger.info("私聊")
        # 获取私聊的用户 ID
        private = event.get_user_id()
        msg_from = "private"

    # 图片路径（前面例子讲过了，自行修改）
    file_path = "./data/template/1.png"
    img_path = Path(file_path)

    # 随便定义了个字符串数组 存两数据演示一下。可以将具体需要发送的文本信息存放到该数组中
    out_str_arr = ["数组中的字符串1", "数组中的字符串2"]
    
    # 定义了一个空的 msgList 列表
    msgList = []

    # 遍历out_str_arr数组
    for out_str in out_str_arr:
        # 将多个元素添加到列表 msgList 中
        # extend() 方法可以接受一个可迭代对象作为参数，如列表、元组或集合等。当该方法被调用时，它将可迭代对象中的所有元素添加到 msgList 列表中。
        msgList.extend(
            [
                # 创建一些自定义的节点，供消息链使用
                MessageSegment.node_custom(
                    user_id=123456, # 转发者的QQ号（随便填）
                    nickname="bot", # 转发者的昵称（随便填）
                    content=Message(MessageSegment.text(out_str)),
                ),
                MessageSegment.node_custom(
                    user_id=1234567,
                    nickname="bot2",
                    content=Message(MessageSegment.image(file=img_path)),
                )
            ]
        )
 
    # 异常捕获
    try:
        # 针对不同的消息来源（群聊或私聊），程序选择调用不同的函数进行消息发送。如果出现异常，则抛出错误提示消息，以便修复问题。
        if msg_from == "group":
            # 转发群聊消息。具体来说，该方法会将 msgList 列表中的信息发送到指定的 group_id 群组中。其中，group_id 表示目标群组的 ID，messages 表示需要发送的消息列表
            await bot.send_group_forward_msg(group_id=group, messages=msgList)
        else:
            # 转发私聊消息。将 msgList 列表中的信息发送到指定的 user_id 用户中。其中，user_id 表示目标用户的 ID，messages 表示需要发送的消息列表
            await bot.send_private_forward_msg(user_id=private, messages=msgList)
    except:
        msg = '果咩，数据发送失败喵~请查看源码和日志定位问题原因'
        await cmd8.finish(msg, reply_message=True)


# 异步 get请求API，API返回一个文本格式的数据，不需要解析，直接utf8解码返回
async def get_api_return_txt(content):
    # 捕获在执行 async with session.get(url=API_URL) 时可能发生的异常，如果发生异常，打印日志并返回 None。
    try:
        # api_url 变量是一个字符串类型的URL地址，用于访问一个API接口。这个API需要传递一个名为 msg 的参数来指定需要计数的文本。
        api_url = 'https://zj.v.api.aa1.cn/api/Age-calculation/?birthday=' + content
        # 异步创建一个HTTP请求会话对象
        async with aiohttp.ClientSession() as session:
            # 向指定的API地址发出GET请求
            async with session.get(url=api_url) as response:
                # 等待结果的返回
                ret = await response.read()
    except Exception as e:
        # nonebot 日志打印下异常，后台方便处理
        nonebot.logger.info(e)
        return None
    
    # 将返回的结果解码为UTF-8格式的字符串，并将其作为函数的返回值。
    return ret.decode('utf-8')


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
