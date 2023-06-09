## 实例 https://github.com/lizhenfen/python/blob/master/Baseinfo/modules/scapy/scap_basic_use.txt

from scapy.all import * # pip install scapy
from IPy import IP as IPTEST # scapy 也存在IP类
import optparse
# linux ttl 值默认 64
# windows ttl值默认 128

ttlValues={}
THRESH=5

def checkTTL(ipsrc,ttl):
    if IPTEST(ipsrc).iptype()=="PRIVATE":
        return
    try:
        #print(ttlValues)
        # python 3 以后删除掉了 has_key 方法
        #if not ttlValues.has_key(ipsrc):
        if ipsrc not in ttlValues:
            pkt=sr1(IP(dst=ipsrc)/ICMP(),retry=0,timeout=1,verbose=0)
            ttlValues[ipsrc]=pkt.ttl
        if abs(int(ttl)-int(ttlValues[ipsrc]))>THRESH:
            print ("\n[!] Detected Possible Spoofed Packet From:"+ipsrc)
            print ('[!] TTl:'+ttl+',Actual TTL:'+str(ttlValues[ipsrc]))
    except Exception as e:
        pass
        #print(e)
        
def testTTL(pkt):
    try:
        if pkt.haslayer(IP):
            ipsrc=pkt.getlayer(IP).src
            ttl=str(pkt.ttl) 
            #print('[+]Pkt Received From :'+ipsrc+",with TTL:"+ttl)
            checkTTL(ipsrc,ttl)
        
    except:
        pass

def main():
    parser=optparse.OptionParser("usage%prog -i<interface> -t <thresh>")
    parser.add_option("-i" ,dest="iface",type="string",help="specify network interface")
    parser.add_option("-d",dest="thresh",type="int",help="specify threshold count")
    (opt,args)=parser.parse_args()
    
    print(conf.ifaces)
    pkt=sr1(IP(dst='8.8.8.8')/ICMP(),retry=0,timeout=1,verbose=0)
    print(pkt)
    print(IP(dst='8.8.8.8'))

    if opt.iface == None:
        conf.iface=conf.ifaces[2]
        #"eth0"
    else:
        conf.iface=opt.iface
    if opt.thresh !=None:
        THRESH=opt.thresh
    else:
        THRESH=5
    sniff(prn=testTTL,store=0)

if __name__ == '__main__':
    main()