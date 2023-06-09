# 检查抓到的包 是否右 某些请求
import dpkt
import socket
import optparse

from pcap import readPcapFile

def findDownload(pcap):
    for (ts,buf) in pcap:
        try:
            
            eth=dpkt.ethernet.Ethernet(buf)
            ip=eth.data 
            src=socket.inet_ntoa(ip.src)
            dst=socket.inet_ntoa(ip.dst) 
            tcp=ip.data 
            http=dpkt.http.Request(tcp.data)
            if(http.method=="GET"):
                uri=http.uri.lower()
                print("url:"+uri)
                print(http.headers)
                if '.zip' in uri and 'loic' in uri:
                    print ('[!]%s Download LOIC.'%(src))
        except Exception  as e: 
            pass

def findGuvenubd(pcap):
    for (ts,buf) in pcap:
        try:
            eth=dpkt.ethernet.Ethernet(buf)
            ip=eth.data
            src=socket.inet_ntoa(ip.src)
            dst=socket.inet_ntoa(ip.dst)

            tcp=ip.data
            dport=tcp.dport
            sport=tcp.sport
            print("dport:%s:%d,sport:%s:%d"%(dst,dport,src,sport))
            if dport ==6667:
                if '!lazor' in tcp.data.lower():
                    print("[!]DDos Hivemind issued by :"+src)
                    print('[+]Target CMD:'+tcp.data)
            if sport ==6667:
                if '!lazor' in tcp.data.lower():
                    print("[!]DDos Hivemind issued to :"+src)
                    print('[+]Target CMD:'+tcp.data)
        except:
            pass

THRESH = 10000
def findAttack(pcap):
    pktCount = {}
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport
            if dport == 80:
                stream = src + ':' + dst
            if pktCount.has_key(stream):
                pktCount[stream] = pktCount[stream] + 1
            else:
                pktCount[stream] = 1
        except:
            pass
    for stream in pktCount:
        pktsSent = pktCount[stream]
        if pktsSent > THRESH:
            src = stream.split(':')[0]
            dst = stream.split(':')[1]
            print('[+] '+src+' attacked '+dst+' with ' + str(pktsSent) + 'pkts.')

def main():
   parser= optparse.OptionParser("using %prog -p <pcap file>")
   parser.add_option("-p",dest="pcapFile",type="string",help="network cap file")
   parser.add_option('-t', dest='thresh', type='int', help='specifythreshold count ')
   (opt,args)=parser.parse_args()
   pcapFile=opt.pcapFile
   if pcapFile ==None:
       print(parser.usage)
       exit(0)
   if opt.thresh != None:
       THRESH = opt.thresh
   else:
        pcap=readPcapFile(pcapFile)  
        findDownload(pcap) 
        findGuvenubd(pcap)
        findAttack(pcap)
        
if __name__ =="__main__":
    main()