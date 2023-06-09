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

while True:
    findDevs()
    time.sleep(5)
    