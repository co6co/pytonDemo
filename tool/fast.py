from scapy.all import *

dnsRecords={}

def handlePkt(pkt):
    if pkt.haslayer(DNSRR):
        rrname=pkt.getlayer(DNSRR).rrname
        rdata=pkt.getlayer(DNSRR).rdata
        if rrname in dnsRecords:
            if rdata not in dnsRecords[rrname]:
                dnsRecords[rrname].append(rdata)
            else:
                dnsRecords[rrname]=[]
                dnsRecords[rrname].append(rdata)

def dnsQRtest(pkt):
    if pkt.haslayer(DNSRR) and pkt .getlayer(UDP).sport == 53:
        rcode = pkt.getlayer(DNS).rcode
        qname=pkt.getlayer(DNSQR).qname
        if rcode==3:
            print("[!] name request lookup failed:"+qname)
            return True
        else :
            return False
def main():
    pkts=rdpcap('fastFlux.pcap')
    for pkt in pkts:
        handlePkt(pkt)
    for item in dnsRecords:
        print ("[+]"+item+"has"+str(len(dnsRecords[item]))+'uniqueIPs.')

    unAnsReqs=0
    pkts=rdpcap('domainFlux.pcap')
    for pkt in pkts:
        if dnsQRtest(pkt):
            unAnsReqs+=1
    print("!"+str(unAnsReqs)+"Total Unanswered Name Requests")
if __name__ == '__main__':
    main()