import requests
from bs4 import BeautifulSoup
import re,sys
sys.path.append("./tool")
from log import log,succ


def _createSoup(url):
    response=requests.get(url,allow_redirects=True) 
    #https://www.jianshu.com/p/424e037c5dd8
    soup=BeautifulSoup(response.text,"html5lib") 
    return soup
def kauiZuiKeji(item): 
    
    url=item["site"]
    arg1=item["arg_1"]
    arg2=item["arg_2"]
    arg3=item["arg_3"]
    log(f"解析{item['remarks']}的订阅地址..{arg1}\t{arg2}\t{arg3}.") 
    soup=_createSoup(url)  
    list=soup.select(arg1)#'a[href*="https://kkzui.com/"]'
    for item in list:
        ret=arg2#"https://kkzui.com/\d+.html"
        m=re.search(ret,item["href"])
        if m:
            url=item["href"]
            return getSubUrl(url,arg3)
    return None

def getSubUrl(href,arg):
    log("嘴科技地址为："+href)
    soup=_createSoup(href) 
    ps=soup.select("p")
    for p in ps:
        if p.string:
            reg=arg #"https://tt.vg/\w+"
            m=re.search(reg,p.string)
            if m:
                #print(f"{m.group()}")
                succ("[+]订阅地址："+m.group())
                return m.group()
            
if __name__ == "__main__":
    url=kauiZuiKeji()
    sub=getSubUrl(url)

    target=f"G:\Tool\SHARE\yaml\cp\subUrl.txt"
    log(f"将订阅地址附加到指定文件。{target}")
   
    f=open(target,"r+",encoding="utf-8")
    allSub=f.read().splitlines()
    if sub not in allSub:allSub.append(sub)
        
    f.seek(0)
    f.truncate()
    content="\n".join(allSub)
    f.write(content)
    f.close()
