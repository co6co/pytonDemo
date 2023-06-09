#coding=UTF-8

import dpkt
import socket
import optparse

import geoip

def printPcap(pcap):
    for (ts,buf) in pcap:
        try:
            eth=dpkt.ethernet.Ethernet(buf)
            ip=eth.data
            src=socket.inet_ntoa(ip.src)
            dst=socket.inet_ntoa(ip.dst)
            print("[+]src:%s[%s]-->dst:%s[%s]"%(src,geoip.getcity(src),dst,geoip.getcity(dst))) 
        except:
            pass

def readPcapFile(pcapPath):
    f=open(pcapPath,'rb')
    head=f.read(4)
    #print(head)
    f.seek(0,0)
    pcap=None
    if head == b'\n\r\r\n':
        pcap = dpkt.pcapng.Reader(f)
    elif head == b'\xd4\xc3\xb2\xa1':
        print(head)
        pcap = dpkt.pcap.Reader(f)
    else:
        print("未知格式")
        exit(0)
    return pcap
def main():
    parser=optparse.OptionParser("use %prog -f <cap file Path>")
    parser.add_option('-F', dest='fileName', type='string',help='specify PDF file name')
    parser.add_option("-f",dest="fileName",type="string",help="cap file path")

    (opt,args)=parser.parse_args()
    fileName=opt.fileName
    if fileName == None:
        print(parser.usage)
        exit(0)
    else:
       pcap=readPcapFile(fileName)
       if pcap !=None:
            printPcap(pcap)
        
if __name__ == '__main__':
    main()