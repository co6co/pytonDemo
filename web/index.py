import mechanize # pip install mechanize //machine
import optparse
# import cookielib # install python 3 移入http 中
from http import cookiejar

from anonBrowser import *

def viewPage(url):
    browser= mechanize.Browser()
    #Mechanize自动遵循robots.txt 这将忽略robots.txt
    browser.set_handle_robots(False)
    #browser.set_handle_equiv(False) 
    page =browser .open(url)
    source_code=page.read()
    print (source_code)

def testProxy(url,proxy,headers):
    browser= mechanize.Browser()
    browser.addheaders=headers
    browser.set_proxies(proxy)
    browser.set_handle_robots(False)
    page =browser .open(url,None,5000)
    source_code=page.read()
    print (source_code)

def printCookies(url):
    browser=mechanize.Browser()
    cookies=cookiejar.LWPCookieJar()
    browser.set_cookiejar(cookies)
    browser.set_handle_robots(False)
    browser.open(url)
    for cookie in cookies:
        print(cookie)

def main():
    parser=optparse.OptionParser("useing %prog -u <url>")
    parser.add_option("-u" ,dest="url",type="string",help="getUrl")
    parser.add_option("-p" ,dest="proxy",type="string",help="proxy address eg. 127.0.0.1:1080")
    (opt,args)=parser.parse_args()
    if opt.url == None:
        print(parser.usage)
        exit(0)
    else:
        hideMeProxy={'socks5':"127.0.0.1:9666"}
        headers=   [{"User-agent","'Mozilla/5.0 (X11; U; Linux 2.4.2-2 i586;en-US; m18) Gecko/20010131 Netscape6/6.01"}]
        #testProxy(opt.url,hideMeProxy,headers)
        #viewPage(opt.url)
        #printCookies(opt.url)

        print("anonBrowser....")
        ab=anonBrowser(proxies=[],user_agents=['User-agent','superSecretBroswer'])
        for attempt in range(1,5):
            ab.anonymize(True)
            print("[*] Fetching page")
            response=ab.open(opt.url)
            for cookie in ab.cookiejar:
                print(cookie)


if  __name__ == "__main__":
    main()