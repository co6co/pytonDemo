import optparse
from scapy.all import *
def inputIface(usageStr):
    print(conf.ifaces)
    parser=optparse.OptionParser("usage%prog -i<interface> "+ usageStr)
    parser.add_option("-i" ,dest="iface",type="string",help="specify network interface")
    return parser

def checkMain():
    if __name__ == "__main__":
        return True
    else:
        return False

