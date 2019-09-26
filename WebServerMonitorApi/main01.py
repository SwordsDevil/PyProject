from WebServerMonitor import transport
import subprocess
import time
#把脚本传过去自动获取信息记录在日志
transport.execute('/root/.ssh/id_rsa','192.168.40.140','root','mkdir /task')
transport.puts('/root/.ssh/id_rsa','192.168.40.140','root','./WebServerMonitor/getInfo.py','/task/getInfo.py')
transport.puts('/root/.ssh/id_rsa','192.168.40.140','root','./agent.py','/task/agent.py')
transport.execute('/root/.ssh/id_rsa','192.168.40.140','root',"echo '*/5 * * * * python3 /task/agent.py &' >>/var/spool/cron/root")
time.sleep(10)
subprocess.run("echo '*/15 * * * * /usr/local/bin/python3.7 /opt/WebServerMonitorApi/main02.py &' >>/var/spool/cron/root",shell=True)