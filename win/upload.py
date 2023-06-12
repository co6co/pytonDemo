
from http.client import HTTPConnection
import time
import re
import os
import optparse 
from urllib.parse import urlparse

#使用服务 vscan.novirusthanks.org 扫描 可执行程序
#用 14 种不同的杀毒引擎扫描
def uploadFile(fileName):
    print("[+] Uploading file to NoVirusThanks...")
    fileContents = open(fileName, 'rb').read() 

    header = {'Content-Type': 'multipart/form-data; boundary=---- WebKitFormBoundaryF17rwCZdGuPNPT9U'}
    params = "------WebKitFormBoundaryF17rwCZdGuPNPT9U"
    params += "\r\nContent-Disposition: form-data;"+"name=\"upfile\"; filename=\""+str(fileName)+"\""
    params += "\r\nContent-Type: "+"application/octetstream\r\n\r\n"
    params += str( fileContents)
    params += "\r\n------WebKitFormBoundaryF17rwCZdGuPNPT9U"
    params += "\r\nContent-Disposition: form-data;"+"name=\"submitfile\"\r\n"
    params += "\r\nSubmit File\r\n"
    params +="------WebKitFormBoundaryF17rwCZdGuPNPT9U--    \r\n"
    conn = HTTPConnection('vscan.novirusthanks.org')
    conn.request("POST", "/", params, header)
    response = conn.getresponse()
    location = response.getheader('location')
    conn.close()
    return location


#我们可以看到服务器返回的构建页面来自：http://vscan.novirusthanks.org +/file/ + md5sum(filecontents) + / + base64(filename)/
#页面返回 HTTP 302 状态码，跳转到 http://vscan.novirusthanks.org + /analysis/+md5sum(file contents) + / + base64(filename)/页面
def printResults(url):
    status = 200
    host = urlparse(url)[1]
    path = urlparse(url)[2]
    if 'analysis' not in path:
        while status != 302:
            conn = HTTPConnection(host)
            conn.request('GET', path)
            resp = conn.getresponse()
            status = resp.status
            print('[+] Scanning file...')
            conn.close()
            time.sleep(15)
    print('[+] Scan Complete.')
    path = path.replace('file', 'analysis')
    conn = HTTPConnection(host)
    conn.request('GET', path)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    reResults = re.findall(r'Detection rate:.*\) ', data)
    htmlStripRes = reResults[1].replace('&lt;font color=\'red\'&gt;','').replace('&lt;/font&gt;', '')
    print('[+] ' + str(htmlStripRes))

def main():
    parser = optparse.OptionParser('usage%prog -f <filename>')
    parser.add_option('-f', dest='fileName', type='string',     help='specify filename')
    (options, args) = parser.parse_args()
    fileName = options.fileName
    if fileName == None:
        print(parser.usage)
        exit(0)
    elif os.path.isfile(fileName) == False:
        print('[+] ' + fileName + ' does not exist.')
        exit(0)
    else:
        loc = uploadFile(fileName)
        printResults(loc)
if __name__ == '__main__':
 main()
