import socket;
import sys;
import os;
from glob import glob
def getFtpBanner(ip,port):
    try:
        socket.setdefaulttimeout(2)
        s=socket.socket()
        s.connect(("127.0.0.1",21))
        rev=s.recv(1024)
        return rev
    except:
        return

def checkVulns(banner):
    bannerFilePath="./file/vuln_banners.txt"
    if os.path.isfile(bannerFilePath):
        print("isFile...........................................................")
    f=open(bannerFilePath,'r')
    for line in f.readlines():
        print(line)
        if line.strip('\n') in str(banner):
            print ("[+] Server is Vulnerable:"+str(banner).strip('\n'))

def baseInfo(): 
    print("__file__:%s"%(__file__))
    print ("当前目录："+os.getcwd())
    print(". absPath:"+os.path.abspath('.'))
    print("../file absPath:"+os.path.abspath('../file'))

    print(". isabs:"+str(os.path.isabs('.')))
    print("../file isabs:"+str(os.path.isabs('../file')))

    #查找文件
    glob('D:/data1/*.tif')

def main():
    ##for x in range (1,255):
    ##    print ("192.168.1."+str(x))
    baseInfo()
    ip="192.168.1.121"
    port=21
    banner=getFtpBanner(ip,port)
    checkVulns(banner)

if __name__=='__main__': 
     if len (sys.argv)==2:
        print("arg0:"+sys.argv[0])
        print("arg1:"+sys.argv[1])
     elif len(sys.argv)==1:
          print("arg0:"+sys.argv[0])
     main()