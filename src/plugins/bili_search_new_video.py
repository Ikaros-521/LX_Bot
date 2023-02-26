import json
import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event
# import nonebot

catch_str = on_command('新视频搜索')

header1 = {
    'cookie': "l=v; PVID=23; _uuid=657CCC62-FE4B-4B4A-7BAD-67239BE354B650516infoc; buvid_fp=a9e08e3c098fe76c72c644c1a5641e03; buvid3=788DBB22-97A9-37BF-D3C8-2E2C985E5E4851060infoc; b_nut=1675953451; buvid4=0068E57C-9762-7898-4F73-0B8994558CF463776-022090818-FRmBv7s%2FltnMkEnT97AnUQ%3D%3D; fingerprint=a9e08e3c098fe76c72c644c1a5641e03; buvid_fp_plain=undefined; LIVE_BUVID=AUTO9316759536885865; i-wanna-go-back=-1; b_ut=5; nostalgia_conf=-1; hit-new-style-dyn=0; hit-dyn-v2=1; CURRENT_FNVAL=4048; bp_video_offset_3493128822589996=760701419143561300; bp_video_offset_3493131139942444=679745700691443700; bp_video_offset_3493121516112620=undefined; bp_video_offset_3493135510407497=760678844795453600; sid=7uyr6wri; rpdid=|(umRRk)R~u|0J'uY~Y|))ku); bp_video_offset_3493135810300442=761281239732715600; is-2022-channel=1; header_theme_version=CLOSE; SESSDATA=d11b13c8%2C1692888711%2Cf50de%2A22; bili_jct=ad8a3f49043c24924bed54a1322c5cce; DedeUserID=3493141460028279; DedeUserID__ckMd5=84bbfcc2a13afc32; innersign=0; b_lsid=9310F6D55_186890F0A04; home_feed_column=4"
}

@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text().strip()

    # print(content)

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
        msg = '传参错误，命令格式【/新视频搜索 关键词 条数】'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    info_json = await get_info(keyword, page_size)
    # nonebot.logger.info(info_json)

    try:
        result = info_json['data']['result']
    except KeyError:
        msg = '\n查询失败，单次查询数最大为50'
        await catch_str.finish(Message(f'{msg}'), at_sender=True)

    msg = "\n 查询内容：" + keyword + "\n" + \
          " 显示格式为：标题 | up | 链接 \n"
    for i in range(len(result)):
        msg += " " + str(result[i]["title"]) + " | " + result[i]["author"] + " | " + str(result[i]["arcurl"]) + ' 】\n'
    await catch_str.finish(Message(f'{msg}'), at_sender=True)


async def get_info(keyword, page_size):
    API_URL = 'https://api.bilibili.com/x/web-interface/search/type?__refresh__=true&page=1&page_size=' + \
              page_size + '&order=pubdate&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword=' + \
              keyword + '&qv_id=nuWZ2YvPoa2tzi16KWQfusc88mDU4m3Y&search_type=video&dynamic_offset=0&preload=true' \
                        '&com2co=true'
    async with aiohttp.ClientSession(headers=header1) as session:
        async with session.get(url=API_URL, headers=header1) as response:
            result = await response.read()
            ret = json.loads(result)
    # nonebot.logger.info(ret)
    return ret
