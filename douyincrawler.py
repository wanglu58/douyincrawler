import datetime
import json
import os
import re
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from dateutil.relativedelta import relativedelta


def get_video(key, value):
    with open(value, 'wb') as v:
        try:
            v.write(requests.get(url=key, headers=headers).content)
            global total_num
            total_num += 1
            return f'{value.split("/")[-1][:-4]} ===> 下载成功。'
        except Exception as e:
            with open(f'{Path}/失败链接.txt', 'a', encoding='utf-8') as f:
                f.write(key)
                f.write('\n')
            return f'{value.split("/")[-1][:-4]} ===> 下载失败。'


awemeurl = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?'
douyinurl = 'https://www.iesdouyin.com/web/api/v2/user/info/?'
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 ' + \
                  '(KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36'
}

string = input('粘贴你要爬取的抖音号的链接：')
issue_start = input('输入你要从哪个时间开始爬取（2018年1月：输入2018.01）回车默认此时间：')
if issue_start == '':
    issue_start = '2018.01'
if issue_start.split('.')[-1][0] == '0':
    month = int(issue_start.split('.')[-1][-1])
else:
    month = int(issue_start.split('.')[-1])
year = int(issue_start.split('.')[0])
current = datetime.date(year, month, 1)
today = datetime.date.today()
timepool = []
while current <= today:
    timepool.append(current.strftime('%Y-%m-%d 00:00:00'))
    current += relativedelta(months=1)
timepool.append(current.strftime('%Y-%m-%d 00:00:00'))

shroturl = re.findall('[a-z]+://[\S]+', string, re.I | re.M)[0]
startpage = requests.get(url=shroturl, headers=headers, allow_redirects=False)
location = startpage.headers['location']
sec_uid = re.findall('(?<=sec_uid=)[a-z，A-Z，0-9, _, -]+', location, re.M | re.I)[0]
getname = requests.get(url=f'{douyinurl}sec_uid={sec_uid}', headers=headers).text
userinfo = json.loads(getname)
name = userinfo['user_info']['nickname']
Path = name

print('\n获取视频链接中，请稍候。。。。。。\n')
json_data = {}
k = len(timepool)
total_num = 0
for i in range(k):
    if i < k - 1:
        beginarray = time.strptime(timepool[i], '%Y-%m-%d %H:%M:%S')
        endarray = time.strptime(timepool[i + 1], '%Y-%m-%d %H:%M:%S')
        t1 = int(time.mktime(beginarray) * 1000)
        t2 = int(time.mktime(endarray) * 1000)

        params = {
            'sec_uid': sec_uid,
            'count': 200,
            'min_cursor': t1,
            'max_cursor': t2,
            'aid': 1128,
            '_signature': 'PtCNCgAAXljWCq93QOKsFT7QjR'
        }

        awemehtml = requests.get(url=awemeurl, params=params, headers=headers).text
        data = json.loads(awemehtml)
        awemenum = len(data['aweme_list'])
        time_str = f"{timepool[i].split('-')[0]}.{timepool[i].split('-')[1]}"
        num = 0
        for i in range(awemenum):
            num += 1
            os.makedirs(f'{Path}/{time_str}-{awemenum}', exist_ok=True)
            videotitle = data['aweme_list'][i].get('desc')
            if not videotitle:
                videotitle = str(uuid.uuid1())
            for s in '\\/:*?\"<>|':
                videotitle = videotitle.replace(s, '')
            videotitle = f'{num}-{videotitle}'
            videourl = data['aweme_list'][i]['video']['play_addr']['url_list'][0]
            json_data[videourl] = f'{Path}/{time_str}-{awemenum}/{videotitle}.mp4'

task_list = []
with ThreadPoolExecutor() as executor:
    for key, value in json_data.items():
        task = executor.submit(get_video, key, value)
        task_list.append(task)
    for res in as_completed(task_list):
        print(res.result())

print(f'\n共下载 {total_num} 个抖音视频，请在当前路径下查看！')
print('Enjoy it')
print('Powered by wanglu58\n')
key = input('按回车键退出\n')
while key != '':
    key = input('按回车键退出\n')
