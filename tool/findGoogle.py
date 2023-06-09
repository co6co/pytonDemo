import optparse
from scapy.all   import *

def findGoogle(pkt):
    if pkt.haslayer(Raw):
        payload = pkt.getlayer(Raw).load
        print(payload)
        if 'GET' in payload:
            if 'google' in payload:
                r = re.findall(r'(?i)\&q=(.*?)\&', payload)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', '    ').replace('%20', ' ')
                    print('[+] Searched For: ' + search)

def main():
    parser = optparse.OptionParser('usage %prog -i <interface>')
    parser.add_option('-i', dest='interface', type='string', help='specifyinterface to listen on')
    print("端口：%s"%(conf.ifaces))
    (options, args) = parser.parse_args()
    if options.interface == None:
        print (parser.usage)
        exit(0)
    else:
        try:
            conf.iface = options.interface
            print('[*] Starting Google Sniffer.')
            sniff(filter='tcp port 443', prn=findGoogle)
        except KeyboardInterrupt:
            exit(0)
if __name__ == '__main__':
  main()