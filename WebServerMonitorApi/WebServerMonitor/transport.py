import paramiko

def puts(RSApath,host,user,localpath,remotepath,port=22,):
    private = paramiko.RSAKey.from_private_key_file(RSApath)
    transport = paramiko.Transport((host,port))
    transport.connect(username=user,pkey=private)
    try:
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(localpath=localpath,remotepath=remotepath)
    finally:
        transport.close()


def execute(RSApath,host,user,command,port=22):
    private = paramiko.RSAKey.from_private_key_file(RSApath)
    transport = paramiko.Transport((host, port))
    transport.connect(username=user, pkey=private)
    client = paramiko.SSHClient()
    client._transport = transport
    try:
        client.exec_command(command=command,timeout=1)
    finally:
        transport.close()