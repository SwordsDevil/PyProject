import paramiko
import json
import pymysql

def getLog(RSApath,host,user,remotepath,localpath,port=22):
    private = paramiko.RSAKey.from_private_key_file(RSApath)
    transport = paramiko.Transport((host,port))
    transport.connect(username=user,pkey=private)

    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remotepath=remotepath,localpath=localpath)
    transport.close()

def operaLogInfo(logpath,logMonitorpath,host,user,password,db):
    with open(file=logpath,mode='r',encoding='utf8') as log:
        for lines in (log.readlines()[-4:]):
            hostname,date=lines.split()[1].lstrip('"').rstrip('",'),lines.split()[2].lstrip('{"').rstrip('":')
            use,system,idle,cpuPercent =lines.split()[5].rstrip(','),lines.split()[7].rstrip(','),\
                                        lines.split()[9].rstrip(','),lines.split()[11].rstrip('},')
            totalM,usedM,freeM,memPercent = lines.split()[14].rstrip(','), lines.split()[16].rstrip(','), \
                                            lines.split()[18].rstrip(','), lines.split()[20].rstrip('},')
            totalD, usedD, freeD, diskPercent = lines.split()[23].rstrip(','), lines.split()[25].rstrip(','), \
                                            lines.split()[27].rstrip(','), lines.split()[29].rstrip('},')

            client = pymysql.connect(host=host, user=user, password=password, db=db)

            try:
                with client.cursor() as cursors:
                    cpuInfo = "insert into cpu values({},'{}',{},{},{},{});"
                    cursors.execute(cpuInfo.format(date, hostname, use, system, idle,cpuPercent))
                client.commit()

                with client.cursor() as cursors:
                    memInfo = "insert into memory values({},'{}',{},{},{},{});"
                    cursors.execute(
                        memInfo.format(date, hostname, totalM, usedM, freeM,memPercent))
                client.commit()

                with client.cursor() as cursors:
                    diskInfo = "insert into disk values({},'{}',{},{},{},{});"
                    cursors.execute(
                        diskInfo.format(date, hostname, totalD, usedD, freeD,diskPercent))
                client.commit()
            finally:
                client.close()

            data = {'hostname':hostname,date:{'cpuPercent':cpuPercent,'memPercent':memPercent,'diskPercent':diskPercent}}
            with open(file=logMonitorpath,mode='a',encoding='utf8') as log:
                json.dump(data,log,ensure_ascii=False)
                log.write('\n')

# operaLogInfo('../log.log','../monitor.log','192.168.40.142','Swords','(Swords..0908)','systemInfo')
