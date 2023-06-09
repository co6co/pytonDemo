# Exif（交换图像文件格式） = JPEG + 拍照参数(光圈、型号、白平衡、ISO、焦距、日期时间及GPS、略缩图)
# 检查所有的Exif信息可能回放回几页的信息，因此只需包含取证有用信息即可；

# coding=utf-8

import urllib3 
from bs4 import BeautifulSoup #pip install beautifulsoup4

from os.path import basename
import urllib.parse
from urllib.parse import urlsplit

from PIL import Image   # install pillow
from PIL.ExifTags import TAGS

import optparse
import os

# 找到网页中的所有图片标签
def findImagesTags(url):
    print('[+] finding images on '+url)
    
    http= urllib3.PoolManager()
    res=http.request('get',url)
    #print("status_code:%d,%s"%( res.status,res.data))
    
    #res=urllib3.PoolManager.urlopen(url= url).read()
    #print("+++++++++%s"%(res))
    soup=BeautifulSoup(res.data)
    imgTags=soup.findAll('img')
    #有的src url
    for imgTag in imgTags:
        imgSrc =imgTag["src"] 
        if(not imgSrc.startswith("http://") and not imgSrc.startswith("https://")):
            urlResult=urllib.parse.urlparse(url)
            imgTag["src"]= urllib.parse.urlunparse([urlResult.scheme,urlResult.netloc,imgSrc,'','',''])
            print(imgTag["src"])

    return imgTags

def downloadImg(imgTag):
    try:
        # 获取图片地址
        imgSrc =imgTag["src"]
        print("[+] Downloading Image...%s"%(imgSrc)) 
        http=urllib3.PoolManager() 
        response=http.request("get",imgSrc)

        if response.status == 200 :
            imgFileName=basename(urlsplit(imgSrc)[2])
            
            dir=  os.path.join(os.path.abspath('../file'),"img")  
            if not os.path.isdir(dir):
                os.makedirs(dir)
            fileFullpath=os.path.join(dir,imgFileName)
            imgFile=open(fileFullpath,'wb')
            imgFile.write(response.data)
            #print("status_code:%d,%s"%( response.status,response.data))
            imgFile.close()
            print("fileFullpath:%s"%(fileFullpath))
            return fileFullpath
        return ""
    except Exception  as e:
        print("error:%s"%(e))
        return ''

def testForExif(imgFileName):
    try:
        print("* exif%s"%(imgFileName))
        exifData={}
        imgFile=Image.open(imgFileName)
        info=imgFile.getexif()
        print(info)
        if info:
            for (tag,vale) in info.items:
                print("tag:%s,vale:%"%(tag,vale))
                decoded=TAGS.get(tag,tag)
                exifData[decoded]=vale
            
            exifGps=exifData["GPSInfo"]
            if exifGps:
                print("[*]"+ imgFileName+ ' contains GPS MetaData')
    except:
        pass

def main():
   # dir=R"H:\Work\Projects\html\python\demo\file\img\52952323737_f25af851c7.jpg"
   # testForExif(dir) 
    parser = optparse.OptionParser('usage%prog -u <target url>')
    parser.add_option('-u', dest='url', type='string', help='specify urladdress')
    (options, args) = parser.parse_args()
    url = options.url
    if url == None:
        print(parser.usage)
        exit(0)
    else:
        imgTags = findImagesTags(url)
        for imgTag in imgTags:
            fileName = downloadImg(imgTag)
            testForExif(fileName)
if __name__ == '__main__':
 main()