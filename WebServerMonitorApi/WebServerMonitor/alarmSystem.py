import yagmail
import requests
import json
import time

def dingTalk(hostname,date,info,percent):
    token = 'adac656b42c272b2e62e5b4e1a0831e431b1bd8d7f23781160d6e856fd32cf3c'
    api = 'https://oapi.dingtalk.com/robot/send?access_token={}'.format(token)
    number = '15779847379'
    header = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": '''主机{}在{}时候
            {}的阈值达到了{}%
            请及时处理
            '''.format(hostname,date,info,percent),
        },
        'at': {
            'atMobiles': [number]
        },
        'isAtAll': False
    }

    sendData = json.dumps(data)
    # for i in range(3):
    requests.post(url=api, data=sendData, headers=header)

def sendEmail(hostname,date,info,percent):
    client = yagmail.SMTP(user='SwordsDevil@163.com',password='cwb0908',host='smtp.163.com')

    content= ['''
    各位运维：
        见信好！我是运维开发的Swords！
        主机为{}在{}时候，
        {}的阈值达到了{}%，
        请及时处理
    '''.format(hostname,date,info,percent)]
    email = '274262321@qq.com'
    client.send(
        to = [email],
        subject = '服务器系统性能达到阈值',
        contents=content
    )

def alarm(logMonitorpth):
    with open(file=logMonitorpth,mode='r',encoding='utf8') as log:

        for lines in (log.readlines()[-4:]):
            hostname= lines.split()[1].lstrip('"').rstrip('",')
            date = lines.split()[2].lstrip('"').rstrip('":')
            cpuPercent = lines.split()[4].lstrip('"').rstrip('",')
            memPercent = lines.split()[6].lstrip('"').rstrip('",')
            diskPercent = lines.split()[8].lstrip('"').rstrip('"}}')
            # print(hostname,date,cpuPercent,memPercent,diskPercent)
            if float(cpuPercent) > 85:
                dingTalk(hostname,date,'cpu',cpuPercent)
                # sendEmail(hostname,date,'cpu',cpuPercent)
            if float(memPercent) > 90:
                dingTalk(hostname,date,'memory',memPercent)
                # sendEmail(hostname, date, 'memory', cpuPercent)
            if float(diskPercent) > 90:
                dingTalk(hostname,date,'disk',diskPercent)
                # sendEmail(hostname, date, 'disk', cpuPercent)

