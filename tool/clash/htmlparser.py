import requests
from bs4 import BeautifulSoup
import re,sys
sys.path.append("./tool")
from log import log


def _createSoup(url):
    response=requests.get(url,allow_redirects=True) 
    #https://www.jianshu.com/p/424e037c5dd8
    soup=BeautifulSoup(response.text,"html5lib") 
    return soup
def getUrl(): 
    log(f"解析快嘴科技的订阅地址...") 
    soup=_createSoup("https://kkzui.com/#term-6")  
    list=soup.select('a[href*="https://kkzui.com/"]')
    for item in list:
        ret="https://kkzui.com/\d+.html"
        m=re.search(ret,item["href"])
        if m:return item["href"]
    return None

def getSubUrl(href):
    log("嘴科技地址为："+href)
    soup=_createSoup(href) 
    ps=soup.select("p")
    for p in ps:
        if p.string:
            reg="https://tt.vg/\w+"
            m=re.search(reg,p.string)
            if m:
                #print(f"{m.group()}")
                log("嘴科技订阅地址："+m.group())
                return m.group()
                  
    
if __name__ == "__main__":
    url=getUrl()
    sub=getSubUrl(url)

    log("将订阅地址附加到指定文件。")
    target=f"G:\Tool\SHARE\yaml\cp\subUrl.txt" 
    f=open(target,"r+",encoding="utf-8")
    allSub=f.read().splitlines()
    if sub not in allSub:
        allSub.append(sub)
        
    f.seek(0)
    f.truncate()
    content="\n".join(allSub)
    f.write(content)
    f.close()
