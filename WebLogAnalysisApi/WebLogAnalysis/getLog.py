import paramiko

def getLog(RSApath,host,user,remotepath,localpath,port=22):
    private = paramiko.RSAKey.from_private_key_file(RSApath)
    transport = paramiko.Transport((host,port))
    transport.connect(username=user,pkey=private)
    try:
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remotepath,localpath)
    finally:
        transport.close()
# getLog('C:\\Users\陈文斌\.ssh\id_rsa','192.168.40.143','root','/var/log/monitor.log','./momitor.log')
