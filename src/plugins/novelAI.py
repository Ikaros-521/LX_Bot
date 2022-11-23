from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import random
import requests
import os, base64
import platform
import json
import time

# 插件依赖 Stable_Diffusion_WebUI
# 用户可以通过 https://github.com/dream80/TonyColab/blob/master/Stable_Diffusion_WebUI(NovelAILeaks).ipynb
# 在colab搭建在线服务，然后将生成的url填入data/novelAI/web_list.txt文件中
# 抓包请求传递的fn_index，填入下方的变量
your_fn_index = 51

# 过滤关键词
htags = ["nsfw", "nude", "without clothes", "sex", "cum_in_mouth", "cum_on_tongue", "facial", "bukkake", "breasts out",
         "nipples", "penis", "ejaculation", "rape", "anal", "double penetration", "pubic tattoo", "vibrator"]
# 冷却时间
novelai_cd = 10
cd = {}
random_num = random.randint(0, 20)
black_list = []

plat = platform.system().lower()
if plat == 'windows':
    # 此处替换你的go-cqhttp路径
    gocqhttp_path = 'F:\\github_pro\\go-cqhttp'
elif plat == 'linux':
    gocqhttp_path = '/root/go-cqhttp'

catch_str = on_keyword({'/novel '})


@catch_str.handle()
async def send_img(bot: Bot, event: Event, state: T_State):
    global htags, novelai_cd, your_fn_index
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    id = event.get_user_id()
    content = get_msg[7:]

    # 判断cd
    nowtime = time.time()
    if (nowtime - cd.get(event.user_id, 0)) < novelai_cd:
        msg = "[CQ:at,qq={}]".format(id) + '你冲的太快啦，请休息一下吧'
        await catch_str.finish(Message(f'{msg}'))
        return
    else:
        cd[event.user_id] = nowtime

    # 检测是否有18+词条
    for i in htags:
        if i in content:
            msg = "[CQ:at,qq={}]".format(id) + '不可以涩涩'
            await catch_str.finish(Message(f'{msg}'))
            return

    urls = await get_url_list_local()
    # nonebot.logger.info(urls)
    if urls[0] == "none":
        msg = "[CQ:at,qq={}]".format(id) + '暂无可用接口，果咩'
        await catch_str.finish(Message(f'{msg}'))
        return

    # 遍历判断黑名单
    for i in urls:
        if i in black_list:
            continue
        else:
            url = i
            break

    out = await get_img(url, your_fn_index, content)
    if out == "error":
        nonebot.logger.info(out)
        out = await get_img(url, your_fn_index, content)
        if out == "error":
            nonebot.logger.info(out)
            msg = "[CQ:at,qq={}]".format(id) + '接口返回错误，获取图片失败'
            await catch_str.finish(Message(f'{msg}'))
            return

    msg = "[CQ:image,file=" + out + "]"
    await catch_str.finish(Message(f'{msg}'))


# 在线获取可用url，暂时好像寄了
async def get_url_list_online():
    API_URL = 'https://api.smoe.me/v1/free'
    ret = requests.get(API_URL)
    ret = ret.json()
    # nonebot.logger.info(ret)
    temp = ["none"]
    try:
        urls_len = len(ret["urls"])
        if urls_len <= 0:
            return temp
        return ret["urls"]
    except KeyError:
        return temp


# 读取本地数据，通过SD-Finder爬取，本地维护
async def get_url_list_local():
    file = open("data/novelAI/web_list.txt", "r")
    lines = file.readlines()
    file.close()

    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')

    # nonebot.logger.info(lines)

    if len(lines) == 0:
        temp = ["none"]
        return temp

    return lines


async def get_img(url, fn_index, content):
    global black_list
    plat = platform.system().lower()

    if plat == 'windows':
        # print('windows系统')
        d = 'data\\'
        out = gocqhttp_path + '\\data\\images\\novel' + str(random_num) + '.png'
    elif plat == 'linux':
        # print('linux系统')
        d = 'data/'
        out = gocqhttp_path + '/data/images/novel' + str(random_num) + '.png'

    # 判断目录是否存在，如果不存在建立目录
    if not os.path.exists(d):
        os.mkdir(d)

    # 如果此接口寄了，通过 https://api.smoe.me/v1/free 获取新接口替换，或本地维护
    # API_URL = url + '/run/predict'
    API_URL = url + 'run/predict'
    nonebot.logger.info(API_URL)
    json1_str = '{"fn_index":' + str(fn_index) + ',"data":["' + content + \
                '","","None","None",20,"Euler a",false,false,1,1,7,-1,-1,0,0,0,false,512,512,false,0.7,0,0,"None",false,false,null,"","Seed","","Nothing","",true,false,false,null,"",""],"session_hash":"9d6qr6oftkh"} '
    json1 = json.loads(json1_str)
    # nonebot.logger.info(json1)
    # 2次超时重试，都失败拉黑
    try:
        ret = requests.post(API_URL, json=json1, timeout=10)
        ret = ret.json()
    except requests.exceptions.RequestException as e:
        nonebot.logger.info(e)
        try:
            ret = requests.post(API_URL, json=json1, timeout=10)
            ret = ret.json()
        except requests.exceptions.RequestException as e:
            nonebot.logger.info(e)
            black_list.append(url)
            return "error"
        except IOError as e:
            nonebot.logger.info(e)
            black_list.append(url)
            return "error"
    except IOError as e:
        nonebot.logger.info(e)
        black_list.append(url)
        return "error"
    # nonebot.logger.info(ret)

    try:
        img_path = ret["data"][0][0]["name"]
        return url + 'file=' + img_path
        # return url + '/file=' + img_path
    except (KeyError, TypeError, IndexError) as e:
        nonebot.logger.info(ret)
        try:
            img_str = ret["data"][0][0]
            img_str = img_str[22:]
        except (KeyError, TypeError, IndexError) as e:
            black_list.append(url)
            return "error"

    # nonebot.logger.info(img_str)

    img_data = base64.b64decode(
        img_str)  # 注意：如果是"data:image/jpg:base64,"，那你保存的就要以png格式，如果是"data:image/png:base64,"那你保存的时候就以jpg格式。
    with open(out, 'wb') as f:
        f.write(img_data)
        f.close()

    return 'novel' + str(random_num) + '.png'
