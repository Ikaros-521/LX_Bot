from playwright.async_api import async_playwright
import re
import base64



async def get_browser():
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context()
    return context  

#判断搜索类型
async def search_confirm(search_input):    
    search_type_base = ['all',2,'prsn','crt',1,4,6]
    search_menu_base = [0,0,1,2,0,0,0]
    search_sort_base = ['subject_search','mono_search','mono_search']

    search_type = search_type_base[search_input]
    search_menu = search_menu_base[search_input]
    search_sort = search_sort_base[search_menu]
    return search_type, search_menu, search_sort



async def bgm_screenshoot1(search_content,search_sort,search_type):
    context = await get_browser()
    page = await context.new_page()
    # await page.goto(f"https://bgm.tv/{search_sort}/{search_content}?cat={search_type}")
    await page.goto(f"https://bgm.tv/{search_sort}/{search_content}?cat={search_type}",wait_until='commit')
    await page.reload()

    #处理网页版面
    content = await page.content()
    pattern = re.compile(r'<div id="columnSearchB"(.*?)<div id="columnSearchC"',re.S)
    content_base = re.search(pattern,content)
    if content_base == None:
        await page.close()
        return None, None

    else:
        content = content_base.group()

        #截图
        image = None
        image = await page.locator('#columnSearchB').screenshot()
        await page.close()
        return base64.b64encode(image).decode(), content



async def bgm_screenshoot2(content,search_menu,browse_num):   
    #处理进一步访问
    context = await get_browser()
    browse_type_base = ["subject","person","character"]
    browse_type = browse_type_base[search_menu]
    pattern_link = re.compile(f'<a href="/{browse_type}/(\d*)"')
    browse_link_base = re.findall(pattern_link,content)
    browse_link = ['ok']
    for i in browse_link_base:
        if browse_link.count(i) < 1:
            browse_link.append(i)
    browse_page = await context.new_page()
    await browse_page.goto(f"https://bgm.tv/{browse_type}/{browse_link[browse_num]}")
   
    #简介栏截图
    image_l = None
    image_l = await browse_page.locator('.infobox').screenshot()   
    
    #收藏盒图r的处理
    if search_menu == 0:
        browse_content= await browse_page.content()
        browse_r = browse_content.replace('<div class="SidePanel png_bg">','<div class="SidePanel png_bg" id="browse_r">')
        await browse_page.set_content(browse_r)

        #收藏盒截图
        image_r = None
        image_r = await browse_page.locator('#browse_r').screenshot()

    await browse_page.close()
    return f"https://bgm.tv/{browse_type}/{browse_link[browse_num]}", base64.b64encode(image_l).decode(), base64.b64encode(image_r).decode()  
