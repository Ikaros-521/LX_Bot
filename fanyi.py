import requests

url = "https://fanyi.qq.com/api/translate"

payload="source=zh&target=jp&sourceText=你好啊&qtv=55cbf2fd1148af1e&qtk=AFOBVuJJRn0fdf1BspBZc1QYJEk0pVZbnGMuRQnsT%2BGFbcmepBgfkB1O9Ofxc39sGYAtYVN1pGIWgSFAU0C6ZdI8k%2FSO93nZhcCL7kDsptPSPNgLy7H2DKoCN8y%2BgbZgBt14rqJO4qAoQ%2BiSsHq5ZA%3D%3D&ticket=&randstr=&sessionUuid=translate_uuid1667118326920"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'fy_guid=e03423fc-712b-4694-853a-ff7d98613298'
}

bytedatas = payload.encode('UTF-8')  #转换编码格式

response = requests.request("POST", url, headers=headers, data=bytedatas)

print(response.text)