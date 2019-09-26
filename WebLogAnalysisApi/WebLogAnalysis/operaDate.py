from WebLogAnalysis.logAnalysis import TotalPUv
from WebLogAnalysis.logAnalysis import TotalTopIp
from WebLogAnalysis.logAnalysis import TotalCode
import requests
import json
import pymysql
import time

def intoMysql(host,user,password,db,allpath):
    date = time.strftime('%Y%m%d%H%M%S')
    client = pymysql.connect(host,user,password,db)

    try:
        with client.cursor() as cursors:
            pv, uv = TotalPUv(allpath)
            PUv = "insert into puv values({},{},{})"
            cursors.execute(PUv.format(date,pv,uv))

        with client.cursor() as cursors:
            TenIp = TotalTopIp(allpath)
            TenIp1 = (str(TenIp[0][0])+'-'+str(TenIp[0][1]))
            TenIp2 = (str(TenIp[1][0]) + '-' + str(TenIp[1][1]))
            TenIp3 = (str(TenIp[2][0]) + '-' + str(TenIp[2][1]))
            TenIp4 = (str(TenIp[3][0]) + '-' + str(TenIp[3][1]))
            Ip = "insert into ip values({},'{}','{}','{}','{}')"
            cursors.execute(Ip.format(date,TenIp1,TenIp2,TenIp3,TenIp4))

        with client.cursor() as cursors:
            totalCode = TotalCode(allpath)
            code = [element[1] for element in totalCode.items()]
            Code = "insert into code values({},{},{},{},{},{},{},{})"
            cursors.execute(Code.format(date,code[0],code[1],code[2],code[3],code[4],code[5],code[6]))
    finally:
        client.commit()
        client.close()
# intoMysql('192.168.40.142','Swords','(Swords..0908)','logInfo',['./access_log'])


def DingTalk(token,allpath):
    api = "https://oapi.dingtalk.com/robot/send?access_token={}".format(token)
    header = {'Content-type':'application/json'}

    date = time.strftime('%Y%m%d%H%M%S')
    pv, uv = TotalPUv(allpath)
    TenIp = TotalTopIp(allpath)
    TenIp1 = (str(TenIp[0][0]) + '-' + str(TenIp[0][1]))
    TenIp2 = (str(TenIp[1][0]) + '-' + str(TenIp[1][1]))
    TenIp3 = (str(TenIp[2][0]) + '-' + str(TenIp[2][1]))
    TenIp4 = (str(TenIp[3][0]) + '-' + str(TenIp[3][1]))

    totalCode = TotalCode(allpath)
    code = [element[1] for element in totalCode.items()]

    # messages = '''date:{}
    #     pv: {} , uv: {},
    #     ipfirst: {}, ipsecond: {}, ipthird: {}, ipfoutth: {},
    #     200: {}, 302: {}, 304: {}, 404: {}, 502: {}, 503: {}, 504: {}
    # '''.format(date, pv, uv, TenIp1, TenIp2, TenIp3, TenIp4, code[0], code[1], code[2], code[3], code[4], code[5],code[6])
    # phone ='15779847379'
    #
    # data = {"msgtype": "text", "text": {"content": "{}".format(messages)}, 'at': {'atMobiles': ["{}".format(phone)]}, 'isAtAll': 'false'}
    phone = '15779847379'
    data = {
         "msgtype": "markdown",
         "markdown": {
             "title":"日志分析报表",
             "text":"#### 分析时间为{} @{}\n".format(date,phone) +
                    "> - pv :{} ,uv : {}\n".format(pv,uv) +
                    "> - ipfirst:{} , ipsecond : {} ,ipthird : {}, ipfourth : {}\n".format(TenIp1, TenIp2, TenIp3, TenIp4) +
                    "> - 200: {} , 302: {} , 304 : {} , 404 : {} , 502 : {} ,503 :{} ,504 : {}".format(code[0], code[1], code[2], code[3], code[4], code[5],code[6])
         },
        "at": {
            "atMobiles": [
                "15779847379"
            ],
            "isAtAll": False
        }
     }

    sendDate = json.dumps(data)

    requests.post(url=api,data=sendDate,headers=header)

# DingTalk('adac656b42c272b2e62e5b4e1a0831e431b1bd8d7f23781160d6e856fd32cf3c',['./access_log'])
