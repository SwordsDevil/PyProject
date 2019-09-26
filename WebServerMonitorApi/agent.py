from WebServerMonitor import getInfo
import subprocess

result = subprocess.run("du -sh /var/log/monitor.log | awk '{print $1}'",shell=True,stdout=subprocess.PIPE)
filesize =result.stdout.decode('utf-8')
filesize = filesize.rstrip("\n")
if filesize == '2.1M':
    subprocess.run("mv /var/log/monitor.{log,log.bak-`date +%Y%m%d%H%M%S`}")
getInfo.intoLog('/var/log/monitor.log')