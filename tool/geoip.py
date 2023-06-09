import pygeoip #>pip install pygeoip
import optparse

# https://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
gi=pygeoip.GeoIP("../file/ip/GeoLiteCity.dat")

def getRecord(ip):
    rec=gi.record_by_addr(ip) 
    #gir = gi.record_by_name("www.google.com") 
    return rec 
def getRecordByHost(host):
    rec=gi.record_by_name(host)  
    return rec

def getcity(ip):
    try:
        rec=gi.record_by_addr(ip) 
        city = rec['city']
        country = rec['country_code3']
        if city != '':
            geoLoc = city + ', ' + country
        else:
            geoLoc = country
        return geoLoc
    except Exception as e: 
        return ''

def printRecord(tgt): 
    ss=getcity(tgt)
    print(ss)
    rec=gi.record_by_addr(tgt)
    
    city=rec['city']
    region=rec['region_code']
    country=rec['country_name']
    long=rec['longitude']
    lat=rec['latitude']
    print("[*] Target:%s Geo-locate."%(tgt))
    print("[*]%s\r\n"%(rec))
    print('[+] '+str(city)+', '+str(region)+', '+str(country))
    print('[+] Latitude: '+str(lat)+ ', Longitude: '+ str(long))

def main():
    parser = optparse.OptionParser('usage %prog -i <ip address >')
    parser.add_option('-i', dest='ipaddress', type='string',help='specify network address')
    (options, args) = parser.parse_args()
    ipaddress = options.ipaddress
    if ipaddress == None:
        print(parser.usage)
        exit(0)
    else:
        printRecord(ipaddress)

if __name__ == '__main__':
    main()

    