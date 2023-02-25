from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random
import re
from typing import List, Tuple
from urllib.parse import quote

import requests

url_init_first = 'https://wallhaven.cc/search?categories=110&purity=100&sorting=random&order=desc&page=1&q='

# 表头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.192 Safari/537.36'
}

catch_str = on_command('搜图WH')


@catch_str.handle()
async def send_msg(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    url = await get_img(content)
    msg = MessageSegment.image(url)
    # msg = "[CQ:image,url=" + url + "]"
    # nonebot.logger.info(msg)
    await catch_str.finish(Message(f'{msg}'))


async def get_page_urls(page_url: str, headers: dict) -> Tuple[List[str], str]:
    """获取当前翻页的所有图片的链接
    Args:
        page_url: 当前翻页的链接
        headers: 请求表头
    Returns:
        当前翻页下的所有图片的链接, 当前翻页的下一翻页的链接
    """
    if not page_url:
        return [], ''
    try:
        html = requests.get(page_url, headers=headers)
        html.encoding = 'utf-8'
        html = html.text
    except IOError as e:
        print(e)
        return [], ''
    pic_urls = re.findall('data-src="(.*?)" ', html, re.S)
    # nonebot.logger.info(pic_urls)
    return pic_urls


async def get_img(keyword: str):
    # 最大下载数量
    # max_download_images = 1

    url_init = url_init_first + quote(keyword, safe='/')
    all_pic_urls = []
    page_urls = await get_page_urls(url_init, headers)
    all_pic_urls.extend(page_urls)
    # nonebot.logger.info(all_pic_urls)

    random_num = random.randint(0, len(page_urls) - 1)

    return page_urls[random_num]

    # page_count = 0  # 累计翻页数

    # 获取图片链接
    # page_urls, next_page_url = get_page_urls(next_page_url, headers)
    # page_count += 1
    # print('正在获取第%s个翻页的所有图片链接' % str(page_count))
    # if next_page_url == '' and page_urls == []:
    # print('已到最后一页，共计%s个翻页' % page_count)
    # all_pic_urls.extend(page_urls)
