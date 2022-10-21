from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import nonebot
import requests

catch_str = on_keyword({'/新视频搜索 '})

header1 = {
    'cookie': 'buvid3=52D30BB7-20FB-C7BA-60B7-EB3F18A8EB9C62437infoc; b_nut=1662632862; i-wanna-go-back=-1; b_ut=5; '
              '_uuid=FB5921023-4BF10-D48E-10A62-EE619E5FA65E60948infoc; buvid_fp=3b2946a9aa52740147f7478c79476df7; '
              'buvid4=0068E57C-9762-7898-4F73-0B8994558CF463776-022090818-FRmBv7s/ltnMkEnT97AnUQ%3D%3D; '
              'fingerprint=eac7b07cd79cd55526b5a7206425ddc6; buvid_fp_plain=undefined; '
              'SESSDATA=89e822a8%2C1678184893%2Cb9824%2A91; bili_jct=3d33d52161227b9ec082ba6124be8d63; '
              'DedeUserID=1123180192; DedeUserID__ckMd5=6b55cc0fe28987d3; sid=8m93076x; PVID=25; '
              'LIVE_BUVID=AUTO9316626329021634; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1663557853,1663637087,'
              '1663811728,1663935967; bp_video_offset_1123180192=707172485766840300; b_lsid=338EE34E_1836A5BC399; '
              '_dfcaptcha=62ba3e19085f0e3de59bc4dcf7663756; innersign=0; '
              'Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1663937476 '
}

@catch_str.handle()
async def send_msg(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())
    # nonebot.logger.info(get_msg)
    content = get_msg[7:]
    # 以空格分割 关键词 条数
    content = content.split()
    keyword = ""
    page_size = "1"

    if len(content) == 1:
        keyword = content[0]
    elif len(content) > 1:
        keyword = content[0]
        page_size = str(int(content[1]))
    else:
        id = event.get_user_id()
        msg = "[CQ:at,qq={}]".format(id) + '传参错误，命令格式【/新视频搜索 关键词 条数】'
        await catch_str.finish(Message(f'{msg}'))
        return

    info_json = await get_info(keyword, page_size)
    # nonebot.logger.info(info_json)

    id = event.get_user_id()

    try:
        result = info_json['data']['result']
    except KeyError:
        msg = "[CQ:at,qq={}]".format(id) + '\n查询失败，单次查询数最大为50'
        await catch_str.finish(Message(f'{msg}'))
        return

    msg = "[CQ:at,qq={}]".format(id) + "\n 查询内容：" + keyword + "\n" + \
          " 显示格式为：标题 | up | 链接 \n"
    for i in range(len(result)):
        msg += " " + str(result[i]["title"]) + " | " + result[i]["author"] + " | " + str(result[i]["arcurl"]) + ' 】\n'
    await catch_str.finish(Message(f'{msg}'))


async def get_info(keyword, page_size):
    API_URL = 'https://api.bilibili.com/x/web-interface/search/type?__refresh__=true&page=1&page_size=' + \
              page_size + '&order=pubdate&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword=' + \
              keyword + '&qv_id=nuWZ2YvPoa2tzi16KWQfusc88mDU4m3Y&search_type=video&dynamic_offset=0&preload=true' \
                        '&com2co=true '
    ret = requests.get(API_URL, headers=header1)
    ret = ret.json()
    # nonebot.logger.info(ret)
    return ret
