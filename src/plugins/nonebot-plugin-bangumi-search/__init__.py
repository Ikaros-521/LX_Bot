from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent, GroupMessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.helpers import HandleCancellation
from nonebot.typing import T_State

from .database import search_confirm, bgm_screenshoot1, bgm_screenshoot2



bgm = on_command(
    "bgm", priority=12
)



@bgm.got(
    "search_content", prompt='请输入要搜索的内容',
    parameterless=[HandleCancellation("已取消")]
)
@bgm.got(
    "search_input", prompt='请输入要搜索的类型编号: \n1.动画 2.现实人物 3.虚拟角色\n4.书籍 5.游戏 6.三次元 0.全部subject', 
    parameterless=[HandleCancellation("已取消")]
)
async def get_search_input(state: T_State):
    search_input_base = str(state["search_input"])
    if search_input_base not in ["0","1","2","3","4","5","6"]:
        await bgm.reject('错误，请重新输入类型编号')
    search_input = int(search_input_base)
    search_content = str(state["search_content"]) 
    state["search_type"], state["search_menu"], state["search_sort"] = await search_confirm(search_input)
    search_sort, search_type = state["search_sort"], state["search_sort"]
    image, state["content"] = await bgm_screenshoot1(search_content,search_sort,search_type)
    if image == None or state["content"] == None:
        await bgm.finish(Message('没有搜索到相关内容哦~'))
    else:
        await bgm.send(MessageSegment.image(f"base64://{image}"), at_sender=True)
        


@bgm.got(
    "browse_num", prompt="请输入你想访问的条目的数字顺序：",
    parameterless=[HandleCancellation("已取消")]
)
async def get_browse_num(state: T_State):
    browse_num_base = str(state["browse_num"])
    if browse_num_base not in ["0","1","2","3","4","5","6","7","8","9","10"]:
        await bgm.reject('错误，请重新输入类型编号')
    browse_num = int(browse_num_base)
    content, search_menu = state["content"], state["search_menu"]
    url, image_l, image_r = await bgm_screenshoot2(content,search_menu,browse_num)
    await bgm.finish(
            f"{url}"
            + MessageSegment.image(f"base64://{image_l}")
            + MessageSegment.image(f"base64://{image_r}"), at_sender=True
            )
