from nonebot.adapters.onebot.v11 import Message
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

cmd1 = on_command('lx', aliases={'LX', '洛曦'})


@cmd1.handle()
async def send_msg(bot: Bot, event: Event):
    msg = '''
【洛曦AI】
洛曦官网：https://ikaros.us.kg/
洛曦 QQ频道：https://pd.qq.com/s/hff4u66vd
洛曦AI QQ群：832618973\n
软件下载：
夸克网盘：https://pan.quark.cn/s/66f5d7a386fb 提取码：HU8s
迅雷网盘：https://pan.xunlei.com/s/VOElCQaY1AOv9YzMqC97C9OeA1 提取码：q8py
百度网盘：https://pan.baidu.com/s/1kHNwVOmWPISar2XLnzLpLQ?pwd=atb7 提取码: atb7\n
通用密钥 测试体验
密钥: gAAAAABnaMF7C-7BLcDg10SLWNslAEZCfm26XPrxKzW7_HxPfYWPshwemqyDmJ8Ix7r-PJ8hFBeJhmdjlz3jwHBuLKxCqSkwRdq2M5oQztlxKHh4jjsfoMXiif9KE9YIsUwtH5UcmLdyafiIk_CFON89fcIr-11hVg==
激活截止时间: 2024-12-30'''

    await cmd1.finish(Message(f'{msg}'))
