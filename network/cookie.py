import re
from scapy.all   import *
import input


cookieTable={}
def  fireCatcher(pkt):
    raw= pkt.sprintf('%Raw.load%')
    r=re.findall("wordpress_[0-9a-fA-F]{32}",raw)
    if r and 'Set' not in raw:
        print (pkt.getlayer(IP).src+">"+pkt.getlayer(IP).dst+" Cookie:"+r[0])
        if r[0] not in cookieTable.keys():
            cookieTable[r[0]]=pkt.getlayer(IP).src
            print ('[+] Detected and indexed cokkie.')
        elif cookieTable[r[0]] != pkt.getlayer(IP).src:
            print ("[*] Detected Conflict for "+r[0])
            print ("Victim="+cookieTable[r[0]])
            print ('Attacker='+ pkt.getlayer(IP).src)

def main(): 
    parser=input.inputIface("")    
    (opt,args)=parser.parse_args()
    if opt.iface == None:
        print(parser.usage)
        exit(0)
    else:
        conf.iface=opt.iface
        sniff(filter="tcp port 80",prn=fireCatcher)

if __name__  =="__main__":
    main()