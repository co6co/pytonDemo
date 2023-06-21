import optparse,os

from bs4 import BeautifulSoup
import re
from anonBrowser import *

    
def _getHtml(url):
    ab =anonBrowser() 
    ab.anonymize()
    page=ab.open(url)
    html=page.read()
    return html

def printLinks(url):
    html =_getHtml(url)
    try:
        link_re=re.compile('href="(.*?)"')
        links=link_re.findall(html)
        for link in links:
            print(link)
    except:
        pass

def printLint2(url):
    html =_getHtml(url)
    try:
        print("\n [+] Printing Links From BeautifulSoup")
        soup=BeautifulSoup(html) 
        links=soup.findAll(name='a')
        for link in links:
            if link.has_key("href"):
                print (link["href"])
    except:
        pass
    

def mirrorImages(url, dir):
 ab = anonBrowser()
 ab.anonymize()
 html = ab.open(url)
 soup = BeautifulSoup(html)
 image_tags = soup.findAll('img')
 for image in image_tags:
    filename = image['src'].lstrip('http://')
    filename = os.path.join(dir, filename.replace('/', '_'))
    print('[+] Saving ' + str(filename))
    data = ab.open(image['src']).read()
    ab.back()
    save = open(filename, 'wb')
    save.write(data)
    save.close()

def main():
    parser = optparse.OptionParser('usage%prog -u <target url>')
    parser.add_option('-u', dest='tgtURL', type='string', help='specify    target url')
    parser.add_option('-d', dest='dir', type='string', help='specifydestination directory')
    (options, args) = parser.parse_args()
    url = options.tgtURL
    dir = options.dir
    if url == None:
        print (parser.usage)
        exit(0)
    else:
        printLinks(url)
        printLint2(url)
        if dir !=None:
            try:
                mirrorImages(url, dir  )
            except Exception as e:
                print('[-] Error Mirroring Images.')
                print('[-] ' + str(e))

if __name__ == '__main__':
    main()
