#from socket import * # gethostbyname(host)
import socket # socket.gethostbyname(host)
import optparse
import threading
# 由于互联网的规模巨大，导致重要信息的片段残留在网上的可能性很高
#打印信号量
screenLock =threading.Semaphore(value=1)

def connScan(host,port):
    try:
        
        connSkt=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connSkt.connect((host,port))
        #connSkt.send('ViolentPython\r\n')
        result=connSkt.recv(100)
        screenLock.acquire() 
        print ('[+]%d/tcp,opened,recv:[%s]'%(port,result))
    except Exception as e:
        screenLock.acquire()
        print('[-]%d/tcp closed.[%s]'%(port,e))
    finally:
        screenLock.release()
        connSkt.close

 
def portScan(hostName,ports): 
    try :
        tgtIP=socket.gethostbyname(hostName )
        print("ip is %s"%(tgtIP))
    except Exception as e:
        print ("[-] Cannot resolve '%s':Unknwn host,%s" %(hostName,e))
        return
    try:
        tgtName=socket.gethostbyaddr(tgtIP)
        print('\n[+] Scan Result For:'+tgtName[0])
    except:
        print ('\n[+] scan Results for :'+tgtIP) 
    socket.setdefaulttimeout(1)
    for tgtPort in ports:
        print("scan %s"%(tgtPort))
        t=threading.Thread(target=connScan,args=(hostName,int(tgtPort)))
        t.start()
        

def main():
    # 解析命令行参数 
    parser=optparse.OptionParser('usage %prog -H <target host> -p <target port>')
    parser.add_option('-H',dest='tgtHost',type='string',help='specify target host')
    parser.add_option('-p',dest='tgtPort',type='int',help='specify target port')
    #
    #args 得到未能解析的参数 包括 -H -p 参数
    (options,args)=parser.parse_args()
    tgtHost=options.tgtHost
    tgtPort=options.tgtPort 
   # args.append(tgtPort)
    args.insert(0,tgtPort) 
    if(tgtHost ==None) | (tgtPort==None):
        print (parser.usage)
        exit(0)
    else:
        print("ip:%s,port=%s"%(tgtHost,args))
        portScan(tgtHost,args)

if __name__ == '__main__':
    main()

