
import optparse
import nmap # pip install python-nmap

def nmapScan(host,port):
    nm=nmap.PortScanner()
    #nm.scan(hosts='127.0.0.1',arguments="-sS -p 22 23 80 443")
    result=nm.scan(host,port)
    #print(result)
    state=result['scan'][host]['tcp'][int(port)]['state']
    print("[*]"+host+" tcp/"+port+" "+state)

def main():
    parser=optparse.OptionParser("usage %prog -H <target host> -p <target port>")
    parser.add_option('-H',dest='tgtHost',type='string',help='specify target host')
    parser.add_option('-p',dest='tgtPort',type='string',help='specify target port')

    (options,args)=parser.parse_args()
    tgtHost=options.tgtHost
    tgtPort=options.tgtPort 
    args.insert(0,tgtPort) 
     
    if(tgtHost ==None) | (tgtPort==None):
        print (parser.usage)
        exit(0)
    else:
        for port in args:
            nmapScan(tgtHost,port) 

if __name__ == '__main__':
 main()
