
def PUv(logpath):
    ips = []
    with open(file=logpath, mode='r', encoding='utf8') as file:
        for lines in file:
            ips.append(lines.split()[0])
    Pv = len(ips)
    Uv = len(set(ips))
    return Pv, Uv

#这里的allpath为一个列表
def TotalPUv(allpath):
    Pv,Uv=0,0
    for logpath in allpath:
        Pv1,Uv1 = PUv(logpath)
        Pv +=Pv1
        Uv +=Uv1
    return Pv,Uv
# Pv,Uv = TotalPUv(['access_log',['access_log']])


def Topip(logpath):
    ips = {}
    with open(file=logpath,mode='r',encoding='utf8') as file:
        for lines in file:
            ips.setdefault(lines.split()[0],0)
            ips[lines.split()[0]] +=1
        ips = sorted(ips.items(),key=lambda x:x[1],reverse=True)
        Tenip = ips[0:10]
    return Tenip

def TotalTopIp(allpath):
    totalIp = {}
    for logpath in allpath:
        Tenip = Topip(logpath)
        for i in range(10):
            totalIp.setdefault(Tenip[i][0],0)
            totalIp[Tenip[i][0]] +=Tenip[i][1]
    totalIp = sorted(totalIp.items(),key=lambda x:x[1],reverse=True)
    totalTenIp = totalIp[0:10]
    return totalTenIp
# TenIp = TotalTopIp(['access_log','access_log'])

def Code(logpath):
    code= {}
    with open(file=logpath,mode='r',encoding='utf8') as file:
        for lines in file:
            key = lines.split()[8]
            for i in ('200', '302', '304', '404', '502', '503', '504'):
                code.setdefault(i,0)
            if key in ('200', '302', '304', '404', '502', '503', '504'):
                code[key] +=1
    # codeAmount = [element[1] for element in code.items()]
    return code


def TotalCode(allpath):
    totalCode = {}
    for logpath in allpath:
        code = Code(logpath)
        for element in code.items():
            totalCode.setdefault(element[0],0)
            totalCode[element[0]] +=element[1]
    return totalCode

# totalCode = TotalCode(['./access_log','access_log'])
# code = [element[1] for element in totalCode.items()]

