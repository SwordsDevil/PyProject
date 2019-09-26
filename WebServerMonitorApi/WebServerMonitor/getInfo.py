import psutil
import pymysql
import subprocess
import time
import json
import paramiko


#获取cpu的use，system，idle和percent信息
def cpu():
    cpuMonitor = psutil.cpu_times_percent()
    use = cpuMonitor.user
    system = cpuMonitor.system
    idle = cpuMonitor.idle
    cpuPercent = float('{:.1f}'.format(use + system))
    return use,system,idle,cpuPercent

def memory():
    memoryMonitor = psutil.virtual_memory()
    totalM = float('{:.1f}'.format(memoryMonitor.total/1024/1024))
    usedM = float('{:.1f}'.format(memoryMonitor.used/1024/1024))
    freeM = float('{:.1f}'.format(memoryMonitor.free/1024/1024))
    memPercent = float('{:.1f}'.format(memoryMonitor.percent))
    return totalM,usedM,freeM,memPercent

def disk():
    diskMonitor = psutil.disk_usage('/')
    totalD = float('{:.1f}'.format(diskMonitor.total/1024/1024/1024))
    usedD = float('{:.1f}'.format(diskMonitor.used/1024/1024/1024))
    freeD = float('{:.1f}'.format(diskMonitor.free/1024/1024/1024))
    diskPercen = float('{:.1f}'.format(diskMonitor.percent))
    return totalD,usedD,freeD,diskPercen

# def intoMysql(host,user,password,db):
#     date = time.strftime('%Y%m%d%H%M%S')
#     hostname = subprocess.run('hostname',shell=True,stdout=subprocess.PIPE)
#
#     client = pymysql.connect(host=host,user=user,password=password,db=db)
#
#     try:
#         with client.cursor() as cursors:
#             use,system,idle,cpuPercent = cpu()
#             cpuInfo = "insert into cpu values({},'{}',{},{},{},{});"
#             cursors.execute(cpuInfo.format(date,hostname.stdout.decode('utf-8').rstrip('\r\n'),use,system,idle,cpuPercent))
#         client.commit()
#
#
#         with client.cursor() as cursors:
#             totalM,usedM,freeM,memPercent = memory()
#             memInfo = "insert into memory values({},'{}',{},{},{},{});"
#             cursors.execute(memInfo.format(date,hostname.stdout.decode('utf-8').rstrip('\r\n'),totalM,usedM,freeM,memPercent))
#         client.commit()
#
#         with client.cursor() as cursors:
#             totalD,usedD,freeD,diskPercent = disk()
#             diskInfo = "insert into disk values({},'{}',{},{},{},{});"
#             cursors.execute(diskInfo.format(date,hostname.stdout.decode('utf-8').rstrip('\r\n'),totalD,usedD,freeD,diskPercent))
#         client.commit()
#     finally:
#         client.close()

def intoLog(logpath):
    date = time.strftime('%Y%m%d%H%M%S')
    hostname = subprocess.run('hostname',shell=True,stdout=subprocess.PIPE)
    use,system,idle,cpuPercent = cpu()
    totalM,usedM,freeM,memPercent=memory()
    totalD,usedD,freeD,diskPercent = disk()
    data = {'hostname': hostname.stdout.decode('utf-8').rstrip('\r\n') ,date: {'cpu': {'use': use ,'system': system ,'idle': idle ,'cpuPercent': cpuPercent },
                  'mem':{'totalM': totalM ,'usedM': usedM ,'freeM': freeM ,'memPercent': memPercent },
                  'disk':{'totalD': totalD ,'usedD': usedD ,'freeD': freeD ,'diskPercent': diskPercent }}}
    with open(file=logpath,mode='a',encoding='utf8') as log:
        json.dump(data, log, ensure_ascii=False)
        log.write('\n')



