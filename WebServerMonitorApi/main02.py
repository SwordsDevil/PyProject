from WebServerMonitor import logAnalysis
from WebServerMonitor import alarmSystem


logAnalysis.getLog('/root/.ssh/id_rsa','192.168.40.140','root','/var/log/monitor.log','/var/log/monitor.log')
logAnalysis.operaLogInfo('/var/log/monitor.log','/var/log/alarm.log','192.168.40.142','Swords','(Swords..0908)','systemInfo')
alarmSystem.alarm('/var/log/alarm.log')