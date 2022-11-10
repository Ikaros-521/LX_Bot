from time import strftime, gmtime
from nonebot import on_command
from nonebot.adapters import Bot, Message
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from httpx import AsyncClient

__plugin_meta__ = PluginMetadata('Apex API Query', 'Apex Legends API 查询插件', '/bridge [玩家名称] 查询玩家信息 \n /maprotation 查询地图轮换 \n /predator 查询 PC 端顶尖猎杀者 \n /crafting 查询制造轮换')

api_key = '22baa40861a1e595b9656caf41dd3e3c'
api_url = 'https://api.mozambiquehe.re/'

player_statistics = on_command('bridge', aliases= {'玩家'})
map_protation = on_command('maprotation', aliases={'地图'})
predator = on_command('predator', aliases={'猎杀'})
crafting_rotation = on_command('crafting', aliases={'制造'})

@player_statistics.handle()
async def _(player_name: Message = CommandArg()):
    service = 'bridge'
    payload = {'auth': api_key, 'player': str(player_name), 'platform': 'PC'}
    await player_statistics.send('正在查询: 玩家 %s' % player_name)
    response = await api_query(service, payload)
    if response:
        if 'Error' in response.json():
            await player_statistics.send('查询失败: %s' % response.json().get('Error'))
        else:
            globals = response.json().get('global')
            realtime = response.json().get('realtime')
            data = ''
            data += '玩家信息: \n'
            data += '名称: %s \n' % str(globals.get('name'))
            data += 'UID: %s \n' % str(globals.get('uid'))
            data += '平台: %s \n' % str(globals.get('platform'))
            data += '等级: %s \n' % str(globals.get('level'))
            data += '封禁状态: %s \n' % str(globals.get('bans').get('isActive'))
            data += '剩余秒数: %s \n' % str(globals.get('bans').get('remainingSeconds'))
            data += '最后封禁原因: %s' % str(convert(globals.get('bans').get('last_banReason')))
            data += '大逃杀段位: %s %s \n' % (str(convert(globals.get('rank').get('rankName'))), str(globals.get('rank').get('rankDiv')))
            data += '大逃杀分数: %s \n' % str(globals.get('rank').get('rankScore'))
            data += '竞技场段位: %s %s \n' % (str(convert(globals.get('arena').get('rankName'))), str(globals.get('arena').get('rankDiv')))
            data += '竞技场分数: %s \n' % str(globals.get('arena').get('rankScore'))
            data += '大厅状态: %s \n' % str(convert(realtime.get('lobbyState')))
            data += '在线: %s \n' % str(convert(realtime.get('isOnline')))
            data += '游戏中: %s \n' % str(convert(realtime.get('isInGame')))
            data += '可加入: %s \n' % str(convert(realtime.get('canJoin')))
            data += '群满员: %s \n' % str(convert(realtime.get('partyFull')))
            data += '已选传奇: %s \n' % str(convert(realtime.get('selectedLegend')))
            data += '当前状态: %s \n' % str(convert(realtime.get('currentState')))
            data += '当前状态时长: %s \n' % str(strftime('%H:%M:%S', gmtime(realtime.get('currentStateSecsAgo'))))
            await player_statistics.send(data)
    else:
        await player_statistics.send('查询失败')

@map_protation.handle()
async def _():
    service = 'maprotation'
    payload = {'auth': api_key, 'verison': '2'}
    await map_protation.send('正在查询: 地图轮换')
    response = await api_query(service, payload)
    if response:
        battle_royale = response.json().get('battle_royale')
        arenas = response.json().get('arenas')
        ranked = response.json().get('ranked')
        arenasRanked = response.json().get('arenasRanked')
        data = ''
        data += '大逃杀: \n'
        data += '当前地图: %s \n' % str(convert(battle_royale.get('current').get('map')))
        data += '下个地图: %s \n' % str(convert(battle_royale.get('next').get('map')))
        data += '剩余时间: %s \n' % str(convert(battle_royale.get('current').get('remainingTimer')))
        data += '竞技场: \n'
        data += '当前地图: %s \n' % str(convert(arenas.get('current').get('map')))
        data += '下个地图: %s \n' % str(convert(arenas.get('next').get('map')))
        data += '剩余时间: %s \n' % str(convert(arenas.get('current').get('remainingTimer')))
        data += '排位赛联盟: \n'
        data += '当前地图: %s \n' % str(convert(ranked.get('current').get('map')))
        data += '下个地图: %s \n' % str(convert(ranked.get('next').get('map')))
        data += '剩余时间: %s \n' % str(convert(ranked.get('current').get('remainingTimer')))
        data += '排位竞技场: \n'
        data += '当前地图: %s \n' % str(convert(arenasRanked.get('current').get('map')))
        data += '下个地图: %s \n' % str(convert(arenasRanked.get('next').get('map')))
        data += '剩余时间: %s \n' % str(convert(arenasRanked.get('current').get('remainingTimer')))
        await map_protation.send(data)
    else:
        await map_protation.send('查询失败')

@predator.handle()
async def _():
    service = 'predator'
    payload = {'auth': api_key}
    await predator.send('正在查询: 顶尖猎杀者')
    response = await api_query(service, payload)
    if response:
        rp = response.json().get('RP')
        ap = response.json().get('AP')
        data = ''
        data += '大逃杀: \n'
        data += 'PC 端: \n'
        data += '猎杀者人数: %s \n' % str(rp.get('PC').get('foundRank'))
        data += '猎杀者分数: %s \n' % str(rp.get('PC').get('val'))
        data += '大师和猎杀者人数: %s \n' % str(rp.get('PC').get('totalMastersAndPreds'))
        data += 'PS4/5 端: \n'
        data += '猎杀者人数: %s \n' % str(rp.get('PS4').get('foundRank'))
        data += '猎杀者分数: %s \n' % str(rp.get('PS4').get('val'))
        data += '大师和猎杀者人数: %s \n' % str(rp.get('PS4').get('totalMastersAndPreds'))
        data += 'Xbox 端: \n'
        data += '猎杀者人数: %s \n' % str(rp.get('X1').get('foundRank'))
        data += '猎杀者分数: %s \n' % str(rp.get('X1').get('val'))
        data += '大师和猎杀者人数: %s \n' % str(rp.get('X1').get('totalMastersAndPreds'))
        data += 'Switch 端: \n'
        data += '猎杀者人数: %s \n' % str(rp.get('SWITCH').get('foundRank'))
        data += '猎杀者分数: %s \n' % str(rp.get('SWITCH').get('val'))
        data += '大师和猎杀者人数: %s \n' % str(rp.get('SWITCH').get('totalMastersAndPreds'))
        data += '竞技场: \n'
        data += 'PC 端: \n'
        data += '猎杀者人数: %s \n' % str(ap.get('PC').get('foundRank'))
        data += '猎杀者分数: %s \n' % str(ap.get('PC').get('val'))
        data += '大师和猎杀者人数: %s \n' % str(ap.get('PC').get('totalMastersAndPreds'))
        data += 'PS4/5 端: \n'
        data += '猎杀者人数: %s \n' % str(ap.get('PS4').get('foundRank'))
        data += '猎杀者分数: %s \n' % str(ap.get('PS4').get('val'))
        data += '大师和猎杀者人数: %s \n' % str(ap.get('PS4').get('totalMastersAndPreds'))
        data += 'Xbox 端: \n'
        data += '猎杀者人数: %s \n' % str(ap.get('X1').get('foundRank'))
        data += '猎杀者分数: %s \n' % str(ap.get('X1').get('val'))
        data += '大师和猎杀者人数: %s \n' % str(ap.get('X1').get('totalMastersAndPreds'))
        data += 'Switch 端: \n'
        data += '猎杀者人数: %s \n' % str(ap.get('SWITCH').get('foundRank'))
        data += '猎杀者分数: %s \n' % str(ap.get('SWITCH').get('val'))
        data += '大师和猎杀者人数: %s \n' % str(ap.get('SWITCH').get('totalMastersAndPreds'))
        await predator.send(data)
    else:
        await predator.send('查询失败')

@crafting_rotation.handle()
async def _():
    service = 'crafting'
    payload = {'auth': api_key}
    await crafting_rotation.send('正在查询: 制造轮换')
    response = await api_query(service, payload)
    if response:
        data = ''
        data += '每日制造: \n'
        data += '%s %s %s 点 \n' % (str(convert(response.json()[0]['bundleContent'][0]['itemType']['name'])), str(convert(response.json()[0]['bundleContent'][0]['itemType']['rarity'])), str(convert(response.json()[0]['bundleContent'][0]['cost'])))
        data += '%s %s %s 点\n' % (str(convert(response.json()[0]['bundleContent'][1]['itemType']['name'])), str(convert(response.json()[0]['bundleContent'][1]['itemType']['rarity'])), str(convert(response.json()[0]['bundleContent'][1]['cost'])))
        data += '每周制造: \n'
        data += '%s %s %s 点\n' % (str(convert(response.json()[1]['bundleContent'][0]['itemType']['name'])), str(convert(response.json()[1]['bundleContent'][0]['itemType']['rarity'])), str(convert(response.json()[1]['bundleContent'][0]['cost'])))
        data += '%s %s %s 点\n' % (str(convert(response.json()[1]['bundleContent'][1]['itemType']['name'])), str(convert(response.json()[1]['bundleContent'][1]['itemType']['rarity'])), str(convert(response.json()[1]['bundleContent'][1]['cost'])))
        data += '赛季制造: \n'
        data += '%s %s %s 点\n' % (str(convert(response.json()[2]['bundleContent'][0]['itemType']['name'])), str(convert(response.json()[2]['bundleContent'][0]['itemType']['rarity'])), str(convert(response.json()[2]['bundleContent'][0]['cost'])))
        data += '%s %s %s 点\n' % (str(convert(response.json()[3]['bundleContent'][0]['itemType']['name'])), str(convert(response.json()[3]['bundleContent'][0]['itemType']['rarity'])), str(convert(response.json()[3]['bundleContent'][0]['cost'])))
        await crafting_rotation.send(data)
    else:
        await crafting_rotation.send('查询失败')

async def api_query(service, payload):
    try:
        async with AsyncClient() as client:
            response = await client.get(api_url + service, params = payload)
        if response.status_code == 200:
            return response
        else:
            return
    except:
        return

def convert(name):
    names = {
        # Map
        'Kings Canyon': '诸王峡谷',
        'World\'s Edge': '世界尽头',
        'Olympus': '奥林匹斯',
        'Storm Point': '风暴点',
        'Broken Moon': '破碎月亮',
        'Encore': '再来一次',
        'Habitat': '栖息地 4',
        'Overflow': '熔岩流',
        'Phase Runner': '相位穿梭器',
        'Party Crasher': '派对破坏者',
        # Barrels
        'barrel_stabilizer': '枪管稳定器',
        'laser_sight': '激光瞄准镜',
        # Mags
        'extended_energy_mag': '加长式能量弹匣',
        'extended_heavy_mag': '加长式重型弹匣',
        'extended_light_mag': '加长式轻型弹匣',
        'extended_sniper_mag': '加长狙击弹匣',
        'shotgun_bolt': '霰弹枪枪栓',
        # Optics
        'optic_hcog_classic': '单倍全息衍射式瞄准镜"经典"',
        'optic_holo': '单倍幻影',
        'optic_variable_holo': '单倍至 2 倍可调节式幻影瞄准镜',
        'optic_hcog_bruiser': '2 倍全息衍射式瞄准镜"格斗家"',
        'optic_sniper': '6 倍狙击手',
        'optic_variable_aog': '2 倍至 4 倍可调节式高级光学瞄准镜',
        'optic_hcog_ranger': '3 倍全息衍射式瞄准镜"游侠"',
        'optic_variable_sniper': '4 倍至 8 倍可调节式狙击手',
        'optic_digital_threat': '单倍数字化威胁',
        'optic_digital_sniper_threat': '4 倍至 10 倍数字化狙击威胁',
        # Hop_Ups
        'anvil_receiver': '铁砧接收器',
        'double_tap_trigger': '双发扳机',
        'skullpiercer_rifling': '穿颅器',
        'turbocharger': '涡轮增压器',
        # Stocks
        'standard_stock': '标准枪托',
        'sniper_stock': '狙击枪枪托',
        # Gear
        'helmet': '头盔',
        'evo_shield': '进化护盾',
        'knockdown_shield': '击倒护盾',
        'backpack': '背包',
        'survival': '隔热板',
        'mobile_respawn_beacon': '移动重生信标',
        # Regen
        'shield_cell': '小型护盾电池',
        'syringe': '注射器',
        'large_shield_cell': '护盾电池',
        'med_kit': '医疗箱',
        'phoenix_kit': '凤凰治疗包',
        'ultimate_accelerant': '绝招加速剂',
        # Ammo
        'special': '特殊弹药',
        'energy': '能量弹药',
        'heavy': '重型弹药',
        'light': '轻型弹药',
        'shotgun': '霰弹枪弹药',
        'sniper': '狙击弹药',
        # Other
        'evo_points': '进化点数',
        'offline': '离线',
        'online': '在线',
        0: '否',
        1: '是',
        'invite': '邀请',
        'open': '打开',
        'inLobby': '在大厅',
        'inMatch': '比赛中',
        'Rare': '稀有',
        'Epic': '史诗',
        'true': '是',
        'false': '否',
        'COMPETITIVE_DODGE_COOLDOWN': '竞技逃跑冷却',
        # Rank
        'Unranked': '菜鸟',
        'Bronze': '青铜',
        'Silver': '白银',
        'Gold': '黄金',
        'Platinum': '白金',
        'Diamond': '钻石',
        'Master': '大师',
        'Apex Predator': 'Apex 猎杀者',
        # Legends
        'Bloodhound': '寻血猎犬',
        'Gibraltar': '直布罗陀',
        'Lifeline': '命脉',
        'Pathfinder': '探路者',
        'Wraith': '恶灵',
        'Bangalore': '班加罗尔',
        'Caustic': '侵蚀',
        'Mirage': '幻象',
        'Octane': '动力小子',
        'Wattson': '沃特森',
        'Crypto': '密客',
        'Revenant': '亡灵',
        'Loba': '罗芭',
        'Rampart': '兰伯特',
        'Horizon': '地平线',
        'Fuse': '暴雷',
        'Valkyrie': '瓦尔基里',
        'Seer': '希尔',
        'Ash': '艾许',
        'Mad Maggie': '疯玛吉',
        'Newcastle': '纽卡斯尔',
        'Vantage': '万蒂奇',
        'Catalyst': '卡特莉丝',
        # Level
        'Common': '等级1',
        'Rare': '等级2',
        'Epic': '等级3',
        'Legendary': '等级4',
        'Mythic': '等级5',
        # Weapon
        'peacekeeper': '和平捍卫者',
        'spitfire': '喷火轻机枪',
    }
    return names.get(name, name)
