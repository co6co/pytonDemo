# coding=UTF-8

import winreg  as _winreg

def val2addr(val):
    addr=""
    #print("%02x"%(val))
    for c in val: 
        addr+=("%02x "%(c-16))
        addr=addr.replace(" ",":")[0:17]
    return addr

def printNets():
    net="SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Signatures\\Unmanaged"
    key=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,net) 

    count = _winreg.QueryInfoKey(key)[0]
    print ('\n[*] Networks You have Joined.')
    for i in range (count):
        try:
            guid= _winreg.EnumKey(key,i) 
            netKey = _winreg.OpenKey(key, str(guid))
          
            (name, addr, tt) = _winreg.EnumValue(netKey, 5)
            #print("name:%s,value:%s，type:%s"%(name,addr,tt))
            (name, name, tt) = _winreg.EnumValue(netKey, 4)
          #  print("%s,%s"%(addr,name))
            macAddr = val2addr(addr)
            netName = str(name)
            print ('[+] "' + netName + '" ' + macAddr )
            _winreg.CloseKey(netKey)
        except Exception as e:
            print(e)
            break

def main():
    printNets()

if __name__ == "__main__":
    main()
