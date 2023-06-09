import bluetooth 
#pip install setuptools==57.5.0

# setuptools 工具包再58版本后 废弃了 use_2to3 方法
# pip install --upgrade setuptools  # 将 setuptools 更新回去


#安装方法
# 下载 master.zip	
# python setup.py install  https://github.com/pybluez/pybluez/blob/master/docs/install.rst
import time

alreadyFound=[]

def findDevs():
    foundDevice=bluetooth.discover_devices(lookup_names=True)
    for (addr,name) in foundDevice:
        if addr not in alreadyFound:
            print("[+]found Bluetooth device "+str(name))
            print ("[+]Mac address:"+str(addr)) 
            alreadyFound.append(addr)
# 建立RFCOMM连接
# 如果连接成功，RFCOMM通道开发且处于监听状态
def rfcommCon(addr,port):
    sock=bluetooth.BluetoothSocket(bluetooth. RFCOMM)
    try:
        sock.connect((addr,port))
        print("[+] RFCOMM port "+str(port)+" optn")
        sock.close()
    except Exception as e:
        print("[-] RFCOMM port "+str(port)+" closed")

# Bluetooth Service Discovery Protocol
# 描述和枚举蓝牙配置文件的类型以及设备提供的服务

def dspBrowse(add):
    services=bluetooth.find_service(address=add)
    for service in services:
        name=service['name']
        proto=service["protocol"]
        port =str (service['port'])
        print ("[+] Found "+str(name)+'on '+str(proto)+":"+port)

while True:
    findDevs()
    time.sleep(5)
    for port in range(1,30):
        for addr in alreadyFound:
            rfcommCon(addr,port)
            dspBrowse(addr)
            
    