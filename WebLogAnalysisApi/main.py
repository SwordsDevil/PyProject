from WebLogAnalysis import getLog
from WebLogAnalysis import operaDate

getLog.getLog(RSApath='',host='',user='root',remotepath='',localpath='')
operaDate.intoMysql(host='192.168.40.142',user='Swords',password='(Swords..0908)',db='logInfo',allpath=['./WebLogAnalysis/access_log'])
operaDate.DingTalk(token='adac656b42c272b2e62e5b4e1a0831e431b1bd8d7f23781160d6e856fd32cf3c',allpath=['./WebLogAnalysis/access_log'])