import json

import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random
import requests
import cv2
import numpy as np
import os
import platform

catch_str = on_keyword({'/r182 '})

headers1 = {
    'Accept': 'application/json, text/plain, */*',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Content-Type': 'text/plain;charset=UTF-8',
    # 'Referer': 'https://live.bilibili.com',
    # 'origin': 'https://live.bilibili.com',
    # 'cookie': "",
    'User-Agent': 'Mozilla/5.0 BiliDroid/6.79.0 (bbcallen@gmail.com) os/android model/Redmi K30 Pro mobi_app/android build/6790300 channel/360 innerVer/6790310 osVer/11 network/2'
}

plat = platform.system().lower()
if plat == 'windows':
    # 此处替换你的go-cqhttp路径
    gocqhttp_path = 'E:\\GitHub_pro\\go-cqhttp'
elif plat == 'linux':
    gocqhttp_path = '/root/go-cqhttp'


@catch_str.handle()
async def send_img(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[6:]

    tag = ""
    r18 = "0"
    # 以空格分割 标签 r18开关
    content = content.split()

    if len(content) > 0:
        tag = content[0]
    if len(content) > 1:
        if content[1] == "1":
            r18 = "1"

    id = event.get_user_id()
    json1 = await get_info(tag, r18)
    try:
        url = json1['data'][0]['urls']['original']
    except KeyError:
        msg = "[CQ:at,qq={}]".format(id) + '搜图出错'
        await catch_str.finish(Message(f'{msg}'))
        return

    file = await make(url)
    file = "out.png"
    msg = "[CQ:image,file=" + file + "]"
    await catch_str.finish(Message(f'{msg}'))


async def get_info(tag, r18):
    API_URL = 'https://api.lolicon.app/setu/v2?tag=' + tag + '&r18=' + r18 + '&?' + str(random.random())
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret


async def get_short_url(src):
    API_URL = 'https://shengapi.cn/api/dwz.php?url=' + src
    ret = requests.get(API_URL)
    ret = ret.text
    # nonebot.logger.info(ret)
    return ret


async def linear_add(pic1, pic2):
    out = pic1 + pic2
    out[out > 255] = 255
    return out


async def divide(pic1, pic2):
    pic2 = pic2.astype(np.float64)
    pic2[pic2 == 0] = 1e-10
    out = (pic1 / pic2) * 255
    out[out > 255] = 255
    return out


async def inversion(pic):
    return 255 - pic


async def rgb2gray(pic):
    pic_shape = pic.shape
    out = np.ones((pic_shape[0], pic_shape[1], 4)) * 255
    temp = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    out[:, :, 0] = temp
    out[:, :, 1] = temp
    out[:, :, 2] = temp
    return out.astype(np.uint8)


async def get_red_channel(pic):
    return pic[:, :, 2]


async def add_alpha(pic, A):
    pic[:, :, 3] = A
    return pic


async def change_color_level(pic, is_light):
    light_table = [120, 120, 121, 121, 122, 122, 123, 123, 124, 124, 125, 125, 126, 126, 127, 127, 128, 128,
                   129, 129, 130, 130, 131, 132, 132, 133, 133, 134, 134, 135, 135, 136, 136, 137, 137, 138,
                   138, 139, 139, 140, 140, 141, 142, 142, 143, 143, 144, 144, 145, 145, 146, 146, 147, 147,
                   148, 148, 149, 149, 150, 150, 151, 152, 152, 153, 153, 154, 154, 155, 155, 156, 156, 157,
                   157, 158, 158, 159, 159, 160, 161, 161, 162, 162, 163, 163, 164, 164, 165, 165, 166, 166,
                   167, 167, 168, 168, 169, 170, 170, 171, 171, 172, 172, 173, 173, 174, 174, 175, 175, 176,
                   176, 177, 177, 178, 179, 179, 180, 180, 181, 181, 182, 182, 183, 183, 184, 184, 185, 185,
                   186, 186, 187, 188, 188, 189, 189, 190, 190, 191, 191, 192, 192, 193, 193, 194, 194, 195,
                   195, 196, 197, 197, 198, 198, 199, 199, 200, 200, 201, 201, 202, 202, 203, 203, 204, 205,
                   205, 206, 206, 207, 207, 208, 208, 209, 209, 210, 210, 211, 211, 212, 212, 213, 214, 214,
                   215, 215, 216, 216, 217, 217, 218, 218, 219, 219, 220, 220, 221, 222, 222, 223, 223, 224,
                   224, 225, 225, 226, 226, 227, 227, 228, 228, 229, 229, 230, 231, 231, 232, 232, 233, 233,
                   234, 234, 235, 235, 236, 236, 237, 237, 238, 239, 239, 240, 240, 241, 241, 242, 242, 243,
                   243, 244, 244, 245, 245, 246, 247, 247, 248, 248, 249, 249, 250, 250, 251, 251, 252, 252,
                   253, 253, 254, 255]
    dark_table = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10,
                  10, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21,
                  22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 32, 32,
                  33, 33, 34, 34, 35, 35, 36, 36, 37, 37, 38, 38, 39, 39, 40, 41, 41, 42, 42, 43, 43,
                  44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 50, 50, 51, 51, 52, 52, 53, 53, 54, 54,
                  55, 55, 56, 56, 57, 57, 58, 59, 59, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 65,
                  66, 66, 67, 68, 68, 69, 69, 70, 70, 71, 71, 72, 72, 73, 73, 74, 74, 75, 75, 76, 77,
                  77, 78, 78, 79, 79, 80, 80, 81, 81, 82, 82, 83, 83, 84, 85, 85, 86, 86, 87, 87, 88,
                  88, 89, 89, 90, 90, 91, 91, 92, 92, 93, 94, 94, 95, 95, 96, 96, 97, 97, 98, 98, 99,
                  99, 100, 100, 101, 102, 102, 103, 103, 104, 104, 105, 105, 106, 106, 107, 107, 108,
                  108, 109, 109, 110, 111, 111, 112, 112, 113, 113, 114, 114, 115, 115, 116, 116, 117,
                  117, 118, 119, 119, 120, 120, 121, 121, 122, 122, 123, 123, 124, 124, 125, 125, 126,
                  127, 127, 128, 128, 129, 129, 130, 130, 131, 131, 132, 132, 133, 133, 134, 135]

    pic_shape = pic.shape
    out = np.zeros((pic_shape[0], pic_shape[1], 4), dtype=np.uint8)
    if is_light:
        out[:, :, 0] = [[light_table[y] for y in x] for x in pic[:, :, 0]]
        out[:, :, 1] = [[light_table[y] for y in x] for x in pic[:, :, 1]]
        out[:, :, 2] = [[light_table[y] for y in x] for x in pic[:, :, 2]]
        out[:, :, 3] = pic[:, :, 3]
    else:
        out[:, :, 0] = [[dark_table[y] for y in x] for x in pic[:, :, 0]]
        out[:, :, 1] = [[dark_table[y] for y in x] for x in pic[:, :, 1]]
        out[:, :, 2] = [[dark_table[y] for y in x] for x in pic[:, :, 2]]
        out[:, :, 3] = pic[:, :, 3]
    return out


async def make(url):
    plat = platform.system().lower()

    if plat == 'windows':
        # print('windows系统')
        d = 'data\\'
        path = 'data\\r18.jpg'
        tgt = 'data\\'
        out = gocqhttp_path + '\\data\\images\\out.png'
    elif plat == 'linux':
        # print('linux系统')
        d = 'data/'
        path = 'data/r18.jpg'
        tgt = 'data/'
        out = gocqhttp_path + '/data/images/out.png'

    # 判断目录是否存在，如果不存在建立目录
    if not os.path.exists(d):
        os.mkdir(d)
    # 通过requests.get获得图片
    r = requests.get(url, headers=headers1)
    r.raise_for_status()
    # 打开要存储的文件，然后将r.content返回的内容写入文件中，因为图片是二进制格式，所以用‘wb’，写完内容后关闭文件，提示图片保存成功
    with open(path, 'wb') as f:
        f.write(r.content)
        f.close()

    hidden_pic = cv2.imread(path)
    hid_shape = hidden_pic.shape
    # nonebot.logger.info(hid_shape)
    # out_shape = (min(sur_shape[0], hid_shape[0]), min(sur_shape[1], hid_shape[1]))
    # surface_pic = cv2.resize(surface_pic, out_shape)
    if hid_shape[0] > hid_shape[1]:
        surface_pic = cv2.imread(tgt + 'tgt_h.png')
    else:
        surface_pic = cv2.imread(tgt + 'tgt_s.png')

    out_shape = (hid_shape[1], hid_shape[0])
    # nonebot.logger.info(sur_shape)
    # nonebot.logger.info(out_shape)
    surface_pic = cv2.resize(surface_pic, out_shape)

    surface_pic = await rgb2gray(surface_pic)
    # cv2.imshow('test', surface_pic)
    # cv2.waitKey(0)
    surface_pic = await change_color_level(surface_pic, True)
    # cv2.imshow('test', surface_pic)
    # cv2.waitKey(0)
    surface_pic = await inversion(surface_pic)
    # cv2.imshow('test', surface_pic)
    # cv2.waitKey(0)

    hidden_pic = await rgb2gray(hidden_pic)
    # cv2.imshow('test', hidden_pic)
    # cv2.waitKey(0)
    hidden_pic = await change_color_level(hidden_pic, False)
    # cv2.imshow('test', hidden_pic)
    # cv2.waitKey(0)

    out_pic = await linear_add(surface_pic, hidden_pic)
    # cv2.imshow('test', out_pic)
    # cv2.waitKey(0)
    A = await get_red_channel(out_pic)
    out_pic = await divide(hidden_pic, out_pic)
    out_pic = await add_alpha(out_pic, A)
    # nonebot.logger.info(type(out_pic))
    cv2.imwrite(out, out_pic, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    return out
